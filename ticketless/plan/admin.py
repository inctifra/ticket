from django.contrib import admin

from .models import Feature
from .models import Plan


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1  # Number of blank feature forms to show
    min_num = 1
    show_change_link = True


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price_percentage")
    list_filter = ("name",)
    search_fields = ("name", "description")
    inlines = [FeatureInline]  # Add Feature inline here


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "plan")
    list_filter = ("plan",)
    search_fields = ("name",)
