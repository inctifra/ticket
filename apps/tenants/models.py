from django.conf import settings
from django.db import models
from django_tenants.models import DomainMixin
from django_tenants.models import TenantMixin
from django_tenants.postgresql_backend.base import _check_schema_name
from tenant_users.tenants.models import TenantBase

class Client(TenantBase):
    name = models.CharField(max_length=100)
    schema_name = models.CharField(
        max_length=63,
        unique=True,
        db_index=True,
        validators=[_check_schema_name],
        help_text="This will act as the subdomain. fidel in fidel.ticket.io",
    )
    created_on = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    auto_create_schema = True
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_tenants",
        help_text="User responsible for managing this tenant."
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_tenants",
        help_text="User who owns this tenant."
    )

    def primary_domain(self):
        return Domain.objects.filter(tenant=self, is_primary=True).first()


class Domain(DomainMixin):
    domain = models.CharField(
        max_length=253,
        unique=True,
        db_index=True,
        help_text=(
            "This include the schema_name and the base domain. i.e fidel.ticket.io",
        ),
    )
