import csv

from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html

from .models import Event
from .models import EventLaunchRequest


@admin.register(EventLaunchRequest)
class EventLaunchRequestAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "subdomain",
        "status",
        "handled",
        "created_at",
        "time_left",
    )
    list_filter = ("status", "handled", "event_type")
    search_fields = ("full_name", "email", "subdomain")

    actions = ["mark_granted", "mark_denied", "mark_cancelled"]

    def mark_granted(self, request, queryset):
        queryset.update(status="G", handled=True)

    mark_granted.short_description = "Mark selected requests as Granted"

    def mark_denied(self, request, queryset):
        queryset.update(status="D", handled=True)

    mark_denied.short_description = "Mark selected requests as Denied"

    def mark_cancelled(self, request, queryset):
        queryset.update(status="C", handled=True)

    mark_cancelled.short_description = "Mark selected requests as Cancelled"

    def time_left(self, obj):
        return obj.time_left

    time_left.short_description = "Time Left"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Advanced, production-ready admin for Event.
    Designed for public schema (shared app) under django-tenants.
    """

    # -----------------------------
    # DISPLAY CONFIG
    # -----------------------------
    list_display = (
        "title",
        "tenant_name",
        "start_at",
        "end_at",
        "duration",
        "venue_name",
        "is_published_badge",
        "capacity",
        "created_at",
    )
    list_display_links = ("title",)
    list_per_page = 25
    ordering = ("-start_at",)
    list_select_related = ("tenant",)

    # -----------------------------
    # FILTERS & SEARCH
    # -----------------------------
    list_filter = (
        "is_published",
        ("start_at", admin.DateFieldListFilter),
        "tenant",
    )
    search_fields = (
        "title",
        "venue_name",
        "venue_address",
        "tenant__name",
    )
    date_hierarchy = "start_at"

    # -----------------------------
    # FIELD ORGANIZATION
    # -----------------------------
    fieldsets = (
        (
            "Event Details",
            {
                "fields": (
                    "tenant",
                    "title",
                    "short_description",
                    ("start_at", "end_at"),
                    ("venue_name", "venue_address"),
                    ("capacity", "is_published"),
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    # -----------------------------
    # CUSTOM COLUMN FORMATTING
    # -----------------------------
    @admin.display(description="Tenant")
    def tenant_name(self, obj):
        return getattr(obj.tenant, "name", str(obj.tenant_id))

    @admin.display(description="Published", boolean=False)
    def is_published_badge(self, obj):
        color = "success" if obj.is_published else "secondary"
        label = "Yes" if obj.is_published else "No"
        return format_html(
            f'<span class="badge bg-{color}" style="padding:4px 8px;">{label}</span>'
        )

    @admin.display(description="Duration")
    def duration(self, obj):
        if obj.start_at and obj.end_at:
            delta = obj.end_at - obj.start_at
            hours = round(delta.total_seconds() / 3600, 1)
            return f"{hours} hrs"
        return "-"

    # -----------------------------
    # CUSTOM ACTIONS
    # -----------------------------
    actions = ["make_published", "make_unpublished", "export_as_csv", "duplicate_event"]

    @admin.action(description="Mark selected events as Published")
    def make_published(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(
            request, f"{updated} event(s) marked as published.", messages.SUCCESS
        )

    @admin.action(description="Mark selected events as Unpublished")
    def make_unpublished(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(
            request, f"{updated} event(s) marked as unpublished.", messages.WARNING
        )

    @admin.action(description="Export selected events as CSV")
    def export_as_csv(self, request, queryset):
        """
        Export selected events to CSV for client sharing/reporting.
        """
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="events.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "ID",
                "Tenant",
                "Title",
                "Start",
                "End",
                "Venue",
                "Capacity",
                "Published",
                "Created",
            ]
        )
        for e in queryset:
            writer.writerow(
                [
                    e.id,
                    getattr(e.tenant, "name", e.tenant_id),
                    e.title,
                    e.start_at,
                    e.end_at,
                    e.venue_name,
                    e.capacity,
                    "Yes" if e.is_published else "No",
                    e.created_at,
                ],
            )
        return response

    @admin.action(description="Duplicate selected events")
    def duplicate_event(self, request, queryset):
        """
        Clone events for quick reuse (without changing tenant or timestamps).
        """
        for e in queryset:
            e.pk = None
            e.id = None
            e.title = f"{e.title} (Copy)"
            e.is_published = False
            e.created_at = timezone.now()
            e.updated_at = timezone.now()
            e.save()
        self.message_user(
            request, f"Duplicated {queryset.count()} event(s).", messages.INFO
        )

    # -----------------------------
    # OPTIMIZATION
    # -----------------------------
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("tenant")
