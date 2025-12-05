from django.contrib import admin

from .models import EventPermission


@admin.register(EventPermission)
class EventPermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "permission")
    list_filter = ("permission", "event")
    search_fields = ("user__email", "event__title")
    ordering = ("event", "user")
    list_per_page = 25
