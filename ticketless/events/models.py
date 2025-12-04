from datetime import timedelta

from django.db import models
from django.utils import timezone

from ticketless.users.models import Profile

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

    full_name = models.CharField(max_length=255)
    plan = models.ForeignKey(
        "plan.Plan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="plan",
    )
    managed_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_requests",
    )
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(
        max_length=128,
        blank=True,
        help_text="This is the password you will use to login into your subdomain",
    )
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
            now = timezone.now()
            self.expires_at = now + timedelta(days=3)

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
