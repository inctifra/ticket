from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.utils.html import format_html

from .models import InventoryBucket
from .models import Order
from .models import OrderItem
from .models import ScanLog
from .models import Ticket
from .models import TicketReservation
from .models import TicketType

# -------------------------------------------------------------------
# INLINE DEFINITIONS
# -------------------------------------------------------------------


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("ticket_type", "quantity", "unit_price", "subtotal_display")

    def subtotal_display(self, obj):
        if obj.unit_price and obj.quantity:
            return f"{obj.unit_price * obj.quantity:.2f}"
        return "-"

    subtotal_display.short_description = "Subtotal"


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0
    readonly_fields = (
        "token",
        "barcode_data",
        "status",
        "issued_at",
        "redeemed_at",
        "event_title",
        "event_start",
    )


# -------------------------------------------------------------------
# TICKET TYPE ADMIN
# -------------------------------------------------------------------


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event_id",
        "price",
        "capacity",
        "per_ticket_capacity",
        "is_active",
        "remaining_display",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "event_id")
    ordering = ("position",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "event_id",
                    "name",
                    "description",
                    "price",
                    "capacity",
                    "per_ticket_capacity",
                    "is_active",
                    "position",
                )
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def remaining_display(self, obj):
        inv = getattr(obj, "inventory", None)
        if not inv:
            return "-"
        color = "green" if inv.remaining > 0 else "red"
        return format_html("<b style='color:{}'>{}</b>", color, inv.remaining)

    remaining_display.short_description = "Remaining"


# -------------------------------------------------------------------
# INVENTORY ADMIN
# -------------------------------------------------------------------


@admin.register(InventoryBucket)
class InventoryBucketAdmin(admin.ModelAdmin):
    list_display = ("ticket_type", "remaining", "reserved", "updated_at")
    list_filter = ("updated_at",)
    search_fields = ("ticket_type__name",)
    readonly_fields = ("updated_at",)


# -------------------------------------------------------------------
# ORDER ADMIN
# -------------------------------------------------------------------


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone",
        "status",
        "total_amount",
        "currency",
        "created_at",
        "paid_at",
    )
    list_filter = ("status", "currency", "created_at")
    search_fields = ("id", "email", "phone")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "paid_at", "meta")
    inlines = [OrderItemInline, TicketInline]

    actions = ["mark_as_refunded", "mark_as_paid"]

    def mark_as_refunded(self, request, queryset):
        updated = queryset.update(status="refunded")
        messages.success(request, f"{updated} order(s) marked as refunded.")

    mark_as_refunded.short_description = "Mark selected orders as Refunded"

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status="paid", paid_at=timezone.now())
        messages.success(request, f"{updated} order(s) marked as Paid.")

    mark_as_paid.short_description = "Mark selected orders as Paid"

    def has_delete_permission(self, request, obj=None):
        # Protect orders from accidental deletion
        return False


# -------------------------------------------------------------------
# TICKET ADMIN
# -------------------------------------------------------------------


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "barcode_display",
        "holder_name",
        "holder_email",
        "ticket_type",
        "status",
        "issued_at",
        "redeemed_at",
        "event_title",
    )
    list_filter = ("status", "issued_at", "redeemed_at")
    search_fields = (
        "holder_name",
        "holder_email",
        "token",
        "barcode_data",
        "event_title",
    )
    date_hierarchy = "issued_at"
    readonly_fields = (
        "id",
        "token",
        "issued_at",
        "redeemed_at",
        "event_title",
        "event_start",
    )

    def barcode_display(self, obj):
        return format_html("<code>{}</code>", obj.barcode_data or obj.token[:8])

    barcode_display.short_description = "Barcode"

    def has_delete_permission(self, request, obj=None):
        # Protect tickets from deletion once issued
        return False


# -------------------------------------------------------------------
# RESERVATION ADMIN
# -------------------------------------------------------------------


@admin.register(TicketReservation)
class TicketReservationAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_type",
        "reserved_quantity",
        "reserved_at",
        "expires_at",
        "order_placeholder",
        "expired_display",
    )
    list_filter = ("reserved_at",)
    search_fields = ("ticket_type__name", "order_placeholder")
    readonly_fields = ("reserved_at",)

    def expired_display(self, obj):
        expired = obj.expires_at < timezone.now()
        color = "red" if expired else "green"
        label = "Expired" if expired else "Active"
        return format_html("<b style='color:{}'>{}</b>", color, label)

    expired_display.short_description = "Status"


# -------------------------------------------------------------------
# SCAN LOG ADMIN
# -------------------------------------------------------------------


@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ("token", "ticket", "scanned_by", "scanned_at", "success", "reason")
    list_filter = ("success", "scanned_at")
    search_fields = ("token", "ticket__holder_name", "scanned_by__username")
    date_hierarchy = "scanned_at"
    readonly_fields = ("scanned_at", "raw_payload")

    def success_icon(self, obj):
        color = "green" if obj.success else "red"
        icon = "✔" if obj.success else "✘"
        return format_html("<b style='color:{}'>{}</b>", color, icon)

    success_icon.short_description = "Valid"
