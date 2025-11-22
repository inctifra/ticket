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

from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html
from django.db import transaction
import csv
import datetime

from .models import Event

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


# ---------------------
# Custom Filters
# ---------------------
class UpcomingFilter(admin.SimpleListFilter):
    title = "When"
    parameter_name = "when"

    def lookups(self, request, model_admin):
        return (
            ("upcoming", "Upcoming (next 30 days)"),
            ("past", "Past"),
            ("today", "Today"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "upcoming":
            return queryset.filter(
                start_at__gte=now, start_at__lte=now + datetime.timedelta(days=30)
            )
        if self.value() == "past":
            return queryset.filter(start_at__lt=now)
        if self.value() == "today":
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + datetime.timedelta(days=1)
            return queryset.filter(start_at__gte=start_of_day, start_at__lt=end_of_day)
        return queryset


# ---------------------
# Admin Actions
# ---------------------
def make_published(modeladmin, request, queryset):
    updated = queryset.update(is_published=True)
    modeladmin.message_user(
        request, f"{updated} event(s) marked as published.", messages.SUCCESS
    )


make_published.short_description = "Mark selected events as published"


def make_unpublished(modeladmin, request, queryset):
    updated = queryset.update(is_published=False)
    modeladmin.message_user(
        request, f"{updated} event(s) marked as unpublished.", messages.SUCCESS
    )


make_unpublished.short_description = "Mark selected events as unpublished"


def export_as_csv(modeladmin, request, queryset):
    """
    Export selected events as CSV. You can expand columns as needed.
    """
    meta = modeladmin.model._meta
    field_names = [
        "id",
        "title",
        "start_at",
        "end_at",
        "venue_name",
        "is_published",
        "capacity",
        "created_at",
        "updated_at",
    ]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f"attachment; filename=events_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = []
        for field in field_names:
            val = getattr(obj, field)
            # format datetimes as ISO if needed
            if isinstance(val, datetime.datetime):
                val = val.isoformat()
            row.append(val)
        writer.writerow(row)
    return response


export_as_csv.short_description = "Export selected events as CSV"


# ---------------------
# Utility / Placeholder for sync logic
# ---------------------
def sync_to_public(event):
    """
    Placeholder: called when an event becomes published. Implement your sync
    to public marketplace here (e.g., enqueue a Celery job, call an API,
    or create/update a row in the public schema).
    """
    # Example: enqueue a task, or call your sync function
    # from .tasks import sync_event_to_public
    # sync_event_to_public.delay(event.pk)
    pass


# ---------------------
# EventAdmin
# ---------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # Columns visible in the changelist
    list_display = (
        "id",
        "title",
        "start_at",
        "end_at",
        "venue_name",
        "display_capacity",
        "is_published",
        "created_at",
        "updated_at",
        "preview_link",
    )

    list_display_links = ("title",)
    list_editable = ("is_published",)  # quick toggle from list view
    list_filter = ("is_published", "venue_name", UpcomingFilter)
    search_fields = ("title", "short_description", "venue_name", "venue_address")
    date_hierarchy = "start_at"
    ordering = ("-start_at",)
    list_per_page = 25

    # Readonly fields in the change form
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # Fields layout in the change form
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("title", "short_description"),
            },
        ),
        (
            "Schedule",
            {
                "fields": ("start_at", "end_at", "capacity"),
                "description": "Set the event times. Use UTC-aware datetimes.",
            },
        ),
        (
            "Venue",
            {
                "fields": ("venue_name", "venue_address"),
            },
        ),
        (
            "Status & Meta",
            {
                "fields": ("is_published", "created_at", "updated_at"),
            },
        ),
    )

    actions = [make_published, make_unpublished, export_as_csv]

    # Helpful small helpers
    def display_capacity(self, obj):
        return obj.capacity or "—"

    display_capacity.short_description = "Capacity"
    display_capacity.admin_order_field = "capacity"

    def preview_link(self, obj):
        """Show a link to preview the event on the tenant site (if applicable)."""
        # If you can generate a preview path for tenant, render it here.
        # Replace '#' with actual URL generation logic.
        url = "#"
        return format_html('<a href="{}" target="_blank">Preview</a>', url)

    preview_link.short_description = "Preview"

    # ---------------------
    # Save hooks - keep fast, minimal DB work here
    # ---------------------
    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """
        Called on save in admin. We can detect publish status transitions and trigger sync.
        Keep heavy work out of the request: enqueue background jobs instead.
        """
        # determine if publish status changed
        was_published = False
        if obj.pk:
            try:
                old = Event.objects.get(pk=obj.pk)
                was_published = old.is_published
            except Event.DoesNotExist:
                was_published = False

        super().save_model(request, obj, form, change)

        # If event transitioned from unpublished -> published, trigger sync
        if not was_published and obj.is_published:
            # enqueue or call sync logic
            sync_to_public(obj)

    # ---------------------
    # Optimize queryset (prefetch if you add related models later)
    # ---------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # if Event had related FK/ManyToMany (tickets, organizer), use select_related/prefetch_related here
        # e.g., qs = qs.select_related('organizer').prefetch_related('tickets')
        return qs

    # ---------------------
    # Optional: Add per-object admin permission checks
    # ---------------------
    def has_change_permission(self, request, obj=None):
        # Example: only superusers can change events; adapt to your RBAC
        if obj is not None and not request.user.is_superuser:
            # optionally add more logic: event owners, tenant staff, etc.
            return True
        return super().has_change_permission(request, obj)

    # ---------------------
    # CSV export in changelist action return
    # ---------------------
    def changelist_view(self, request, extra_context=None):
        # Keep default behaviour, but you could inject extra context like counts
        return super().changelist_view(request, extra_context=extra_context)


# Optional: register ModelAdmin for other related models (tickets, orders) similarly.
