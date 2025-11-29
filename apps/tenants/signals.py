from django.dispatch import receiver
from django_tenants.signals import post_schema_sync
from django_tenants.signals import schema_migrate_message
from django_tenants.signals import schema_needs_to_be_sync
from django.db.models.signals import post_save
from .models import Client
from django.dispatch import receiver
from django_tenants.signals import post_schema_sync
from .utils import create_tenant_superuser


# @receiver(post_save, sender=Client)
# def handle_schema_migrated(sender, **kwargs):
#     if kwargs.get("created", False):
#         tenant = kwargs.get("instance")
#         print(f"New tenant created: {tenant.schema_name}")



# @receiver(post_schema_sync)
# def auto_create_tenant_superuser(sender, **kwargs):
#     tenant = kwargs["tenant"]
#     print(tenant)


