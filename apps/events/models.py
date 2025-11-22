from django.db import models


from django.db import models
from django.utils import timezone
from datetime import timedelta

EVENT_TYPES = [
    ("concert", "Concert / Festival"),
    ("conference", "Conference / Expo"),
    ("training", "Training / Workshop"),
    ("church", "Church / Charity Event"),
    ("sports", "Sports / Tournament"),
    ("other", "Other"),
]

STATUS_CHOICES = [
    ("G", "Granted"),
    ("P", "Processing"),
    ("D", "Denied"),
    ("C", "Cancelled"),
]


class EventLaunchRequest(models.Model):
    full_name = models.CharField(max_length=255)
    plan = models.ForeignKey(
        "plan.Plan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan",
    )
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    subdomain = models.CharField(max_length=50, unique=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    event_details = models.TextField(blank=True)

    handled = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="P")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.full_name} ({self.subdomain}.ticketless.io)"

    def save(self, *args, **kwargs):
        # Set default expiry to 3 days after creation if not set
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(days=3)

        # Automatically mark handled if status is Granted, Denied, or Cancelled
        if self.status in ["G", "D", "C"]:
            self.handled = True
        else:
            self.handled = False

        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Check if request is expired based on expires_at"""
        return timezone.now() > self.expires_at

    @property
    def time_left(self):
        """Returns remaining time until expiry"""
        remaining = self.expires_at - timezone.now()
        if remaining.total_seconds() < 0:
            return "Expired"
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"


class Event(models.Model):
    """
    Canonical event record, visible on the public marketplace.
    Each Event belongs to a tenant (owner).
    """

    id = models.BigAutoField(primary_key=True)
    tenant = models.ForeignKey(
        "tenants.Client", on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField(max_length=255)
    short_description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, blank=True)
    venue_address = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Denormalized fields helpful for listing
    capacity = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["start_at"]),
            models.Index(fields=["tenant"]),
            models.Index(fields=["is_published"]),
        ]
        ordering = ["-start_at"]

    def __str__(self):
        return f"{self.title} ({self.start_at.date()})"
