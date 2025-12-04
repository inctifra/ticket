from django.contrib import admin

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
