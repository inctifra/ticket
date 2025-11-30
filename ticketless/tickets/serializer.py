from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import InventoryBucket
from .models import Order
from .models import OrderItem
from .models import ScanLog
from .models import Ticket
from .models import TicketReservation
from .models import TicketType

User = get_user_model()


class TicketTypeSerializer(serializers.ModelSerializer):
    """Serializer for TicketType model."""

    event_id = serializers.IntegerField(help_text="ID of event in public schema.")
    total_capacity = serializers.SerializerMethodField()

    class Meta:
        model = TicketType
        fields = [
            "id",
            "event_id",
            "name",
            "description",
            "capacity",
            "per_ticket_capacity",
            "price",
            "is_active",
            "position",
            "created_at",
            "updated_at",
            "total_capacity",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "total_capacity"]

    def get_total_capacity(self, obj):
        if obj.capacity and obj.per_ticket_capacity:
            return obj.capacity * obj.per_ticket_capacity
        return obj.capacity


class InventoryBucketSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(read_only=True)
    ticket_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(), source="ticket_type", write_only=True
    )

    class Meta:
        model = InventoryBucket
        fields = [
            "id",
            "ticket_type",
            "ticket_type_id",
            "remaining",
            "reserved",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]


class OrderItemSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(read_only=True)
    ticket_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(),
        source="ticket_type",
        write_only=True,
        help_text="TicketType being purchased",
    )

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "ticket_type",
            "ticket_type_id",
            "quantity",
            "unit_price",
            "subtotal",
        ]
        read_only_fields = ["id", "subtotal"]

    def get_subtotal(self, obj):
        return obj.quantity * obj.unit_price


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "email",
            "phone",
            "status",
            "status_display",
            "total_amount",
            "currency",
            "created_at",
            "paid_at",
            "meta",
            "items",
        ]
        read_only_fields = ["id", "created_at", "paid_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)

        # Create items and compute total
        total = 0
        for item_data in items_data:
            order_item = OrderItem.objects.create(order=order, **item_data)
            total += order_item.quantity * order_item.unit_price

        order.total_amount = total
        order.save(update_fields=["total_amount"])
        return order


class TicketSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(read_only=True)
    ticket_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(), source="ticket_type", write_only=True
    )
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    is_redeemable = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "order",
            "ticket_type",
            "ticket_type_id",
            "holder_name",
            "holder_email",
            "token",
            "barcode_data",
            "status",
            "issued_at",
            "redeemed_at",
            "event_title",
            "event_start",
            "is_redeemable",
        ]
        read_only_fields = [
            "id",
            "token",
            "barcode_data",
            "issued_at",
            "redeemed_at",
            "event_title",
            "event_start",
        ]

    def get_is_redeemable(self, obj):
        return obj.status == "issued"


class TicketReservationSerializer(serializers.ModelSerializer):
    ticket_type = TicketTypeSerializer(read_only=True)
    ticket_type_id = serializers.PrimaryKeyRelatedField(
        queryset=TicketType.objects.all(), source="ticket_type", write_only=True
    )
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = TicketReservation
        fields = [
            "id",
            "ticket_type",
            "ticket_type_id",
            "reserved_quantity",
            "reserved_at",
            "expires_at",
            "order_placeholder",
            "is_expired",
        ]
        read_only_fields = ["id", "reserved_at", "is_expired"]

    def get_is_expired(self, obj: TicketReservation):
        return obj.expires_at < timezone.now()


class ScanLogSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)
    scanned_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ScanLog
        fields = [
            "id",
            "ticket",
            "token",
            "scanned_by",
            "scanned_at",
            "success",
            "reason",
            "raw_payload",
        ]
        read_only_fields = ["id", "scanned_at"]
