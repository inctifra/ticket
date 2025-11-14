from django.db import models


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
