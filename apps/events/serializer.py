from rest_framework import serializers
from tenants.models import Client

from .models import Event


class TenantMiniSerializer(serializers.ModelSerializer):
    """Lightweight tenant serializer for public display."""

    class Meta:
        model = Client
        fields = ["id", "name", "schema_name", "created_on"]
        read_only_fields = fields


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event model with robust validation and
    nested tenant representation for read operations.
    """

    tenant = TenantMiniSerializer(read_only=True)
    tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source="tenant",
        write_only=True,
        required=True,
        help_text="The tenant who owns this event.",
    )

    duration_hours = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "tenant",
            "tenant_id",
            "title",
            "short_description",
            "start_at",
            "end_at",
            "venue_name",
            "venue_address",
            "capacity",
            "is_published",
            "created_at",
            "updated_at",
            "duration_hours",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "duration_hours"]

    def get_duration_hours(self, obj):
        """Compute event duration (in hours) if both start and end are defined."""
        if obj.start_at and obj.end_at:
            return round((obj.end_at - obj.start_at).total_seconds() / 3600, 2)
        return None

    def validate(self, data):
        """
        Cross-field validation: ensure end time is after start time,
        and required fields are coherent.
        """
        start = data.get("start_at", getattr(self.instance, "start_at", None))
        end = data.get("end_at", getattr(self.instance, "end_at", None))

        if end and start and end <= start:
            raise serializers.ValidationError(
                {"end_at": "Event end time must be after start time."}
            )

        capacity = data.get("capacity", getattr(self.instance, "capacity", None))
        if capacity is not None and capacity < 0:
            raise serializers.ValidationError(
                {"capacity": "Capacity cannot be negative."}
            )

        return data

    def create(self, validated_data):
        """Custom creation logic with audit logging (optional)."""
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Ensure safe updates and partial field control."""
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
