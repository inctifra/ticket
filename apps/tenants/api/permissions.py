from rest_framework.permissions import BasePermission
from django.db import connection
from apps.tenants.models import Client
from rest_framework.exceptions import PermissionDenied


class TenantHeaderPermission(BasePermission):
    """
    If X-Tenant header exists, validate it and set request.tenant.
    Otherwise, allow request to proceed.
    """

    def has_permission(self, request, view):
        schema = request.headers.get("X-Tenant")

        if not schema:
            msg = "You must provide the X-Tenant header"
            raise PermissionDenied(msg)
        try:
            tenant = Client.objects.get(schema_name=schema)
        except Client.DoesNotExist:
            msg = f"Tenant '{schema}' does not exist"
            raise PermissionDenied(msg) from None
        connection.set_tenant(tenant)
        request.tenant = tenant
        return True
