import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TicketType(models.Model):
    """
    Types of tickets for an event (e.g., single, group of 5, VIP).
    Lives in tenant schema. Links to public Event by id (no FK).
    """

    id = models.BigAutoField(primary_key=True)
    event_id = (
        models.BigIntegerField()
    )  # integer PK of public Event (denormalized link)
    name = models.CharField(max_length=120)  # e.g., "Group (5)"
    description = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )  # max number of *tickets* of this type
    per_ticket_capacity = models.PositiveIntegerField(
        default=1,
        help_text="Ticket can carry multiple users",
    )  # if seats per ticket (group of 5 -> 5)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)  # ordering in UI
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["event_id"]),
            models.Index(fields=["id"]),
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
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="This field is not required since we won't be registering users",
    )  # optional guest purchases
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=(
            ("pending", "Pending Payment"),
            ("paid", "Paid"),
            ("cancelled", "Cancelled"),
            ("refunded", "Refunded"),
        ),
        default="pending",
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    # store gateway metadata
    meta = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"Order for {self.email} {self.phone}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [models.Index(fields=["ticket_type"])]

    def __str__(self):
        return str(self.ticket_type.name)


class Ticket(models.Model):
    """
    Actual ticket issued to customer. Contains a barcode/QR token
    and scanning status. Use non-sequential secure token.
    """

    STATUS_CHOICES = [
        ("issued", "Issued"),
        ("redeemed", "Redeemed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    holder_name = models.CharField(max_length=255, blank=True)
    holder_email = models.EmailField(blank=True)
    token = models.CharField(
        max_length=128,
        unique=True,
    )  # e.g., signed token or base32
    barcode_data = models.CharField(
        max_length=255,
        blank=True,
    )  # friendly code for scanning (human-readable)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="issued")
    issued_at = models.DateTimeField(auto_now_add=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)
    # Denormalized snapshot of event for fast lookup at scan time:
    event_title = models.CharField(max_length=255, blank=True)
    event_start = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return str(self.holder_name)


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
    )  # link to pending order id

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
    )  # scanned token
    scanned_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    scanned_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    reason = models.CharField(max_length=255, blank=True, help_text="redeemed")
    raw_payload = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.token
