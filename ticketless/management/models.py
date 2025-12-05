from django.db import models

from ticketless.tickets.models import User


class EventPermission(models.Model):
    PERMISSION_CHOICES = [
        ("scan_tickets", "Can scan tickets"),
        ("manage_event", "Can manage event"),
        ("view_reports", "Can view event reports"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_permissions"
    )
    event = models.ForeignKey(
        "tickets.Event", on_delete=models.CASCADE, related_name="permissions"
    )
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event", "permission"],
                name="unique_event_user_permission",
            ),
        ]

    def __str__(self):
        return self.get_permission_display()
