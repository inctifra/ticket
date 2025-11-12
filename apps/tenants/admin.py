from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Client
from .models import Domain


class DomainStackedInlineAdmin(admin.StackedInline):
    model = Domain
    extra = 0


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ["schema_name", "name", "created_on"]
    inlines = [DomainStackedInlineAdmin]
