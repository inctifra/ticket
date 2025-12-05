from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import Profile
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ("email", "name", "is_active")
    list_filter = ("is_active",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Tenant Info", {"fields": ("is_active",)}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )

    search_fields = ("email", "name")
    ordering = ("email",)
    filter_horizontal = ()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "role", "updated_at")
    search_fields = ("user__email",)
    list_filter = ("created_at", "updated_at", "role")
    autocomplete_fields = ("user",)
