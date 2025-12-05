import uuid
from io import BytesIO

import qrcode
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from ticketless.tickets.utils import upload_event_image_path

User = get_user_model()


class Event(models.Model):
    """
    Event stored inside tenant schema, isolated per tenant.
    This event is *NOT* visible to public schema without syncing.
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    short_description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, blank=True)
    venue_address = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    cover = models.ImageField(upload_to="event_covers/", null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["start_at"]),
            models.Index(fields=["is_published"]),
        ]
        ordering = ["-start_at"]

        permissions = [
            ("manage_event", "Can manage event and ticket types"),
            ("view_event_reports", "Can view event sales and attendance reports"),
            ("scan_tickets", "Can scan tickets at event entry"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_at__gte=models.F("start_at")),
                name="end_after_start",
            ),
            models.UniqueConstraint(
                fields=["title", "start_at"],
                name="unique_event_title_start",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.start_at.date()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(slugify(self.title) + str(uuid.uuid4()))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tenants:event_detail", kwargs={"slug": self.slug})

    @property
    def is_expired(self):
        """
        Returns True if the event has already ended.
        Returns False if the event has no end date or is still upcoming.
        """
        if not self.end_at:
            return False
        return timezone.now() > self.end_at

    @property
    def duration(self):
        """
        Returns the duration of the event as a timedelta object.
        If end_at is not set, returns None.
        """
        if self.end_at:
            return self.end_at - self.start_at
        return None

    @property
    def duration_str(self):
        """
        Returns a human-readable duration string like '1h 30m'.
        """
        if not self.end_at:
            return "N/A"

        delta = self.end_at - self.start_at
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []
        if hours:
            parts.append(f"{hours} h")
        if minutes:
            parts.append(f"{minutes} m")
        return " ".join(parts)


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_event_image_path)
    alt_text = models.CharField(max_length=255, blank=True)
    ordering = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Image for {self.event.title}"


class TicketType(models.Model):
    """
    Types of tickets for an event (e.g., single, group of 5, VIP).
    Lives in tenant schema. Links to public Event by id (no FK).
    """

    id = models.BigAutoField(
        primary_key=True, editable=False, unique=True, db_index=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="event_ticket_type",
    )
    name = models.CharField(max_length=120)  # e.g., "Group (5)"
    description = models.TextField(blank=True)
    per_ticket_capacity = models.PositiveIntegerField(
        default=1,
        help_text="Ticket can carry multiple users",
    )  # if seats per ticket (group of 5 -> 5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_id"]),
            models.Index(fields=["id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["event", "name", "id"],
                name="unique_event_ticket_type_name",
            ),
        ]

    def __str__(self):
        return f"{self.name} — {self.price}"


class InventoryBucket(models.Model):
    """
    Tracks remaining capacity for a ticket type.
    Use DB transactions/row-locking to modify atomically.
    """

    ticket_type = models.OneToOneField(
        TicketType,
        on_delete=models.CASCADE,
        related_name="inventory",
    )
    remaining = models.IntegerField()
    # optional: reserved_count for currently reserved but unpaid tickets
    reserved = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inventory <Remaining: {self.remaining} Reserved: {self.reserved}>"


class Order(models.Model):
    """
    Customer order. Contains OrderItems. One order may result in multiple Tickets.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # optional guest purchases
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="This field is not required since we won't be registering users",
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=(
            ("pending", "Pending Payment"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
            ("refunded", "Refunded"),
            ("failed", "Failed"),
        ),
        default="pending",
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Order for {self.email} {self.phone}"

    def delete_url(self):
        return reverse(
            "tenants:actions:delete_order_view", kwargs={"order_id": str(self.id)}
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=["ticket_type"])]

    def __str__(self):
        return str(self.ticket_type.name)


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("issued", "Issued"),
        ("redeemed", "Redeemed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_item = models.ForeignKey(
        "OrderItem",
        related_name="tickets",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    holder_name = models.CharField(max_length=255, blank=True)
    holder_email = models.EmailField(blank=True)
    seats = models.PositiveIntegerField(default=1)
    token = models.CharField(max_length=128, unique=True, blank=True, null=True)
    scan_token = models.CharField(max_length=128, unique=True, blank=True, null=True)
    barcode_data = models.CharField(max_length=255, blank=True)
    qr_code = models.ImageField(upload_to="tickets/qrcodes/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="issued")
    issued_at = models.DateTimeField(auto_now_add=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    event_title = models.CharField(max_length=255, blank=True)
    event_start = models.DateTimeField(null=True, blank=True)
    sent_mail = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.holder_name or str(self.id)

    # -----------------------
    # QR CODE AUTO GENERATION
    # -----------------------
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(self.token)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"{self.token}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)


class TicketReservation(models.Model):
    """
    Short-lived reservation to hold inventory while checkout happens.
    Use expiry and periodic cleanup.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    reserved_quantity = models.PositiveIntegerField()
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    order_placeholder = models.UUIDField(
        null=True,
        blank=True,
    )

    class Meta:
        indexes = [models.Index(fields=["expires_at"])]

    def __str__(self):
        return self.ticket_type.name


class ScanLog(models.Model):
    """
    Audit log for every scan attempt at entry.
    """

    id = models.BigAutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    token = models.CharField(
        max_length=128,
        help_text="The scanned ticket token",
    )
    scanned_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    scanned_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    reason = models.CharField(max_length=255, blank=True, help_text="redeemed")
    raw_payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.token
