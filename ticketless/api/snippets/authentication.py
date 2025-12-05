from django.db import connection
from django_tenants.utils import get_tenant_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TenantHeaderAuthentication(BaseAuthentication):
    """
    Reads 'X-Tenant' from the request header and switches the tenant schema.
    Only applied to API views that include this authentication class.
    """

    def authenticate(self, request):
        tenant_header = request.headers.get("X-Tenant")
        if not tenant_header:
            msg = "X-Tenant header missing"
            raise AuthenticationFailed(msg)
        tenant_header = str(tenant_header).lower()
        tenant_model = get_tenant_model()
        try:
            tenant = tenant_model.objects.get(schema_name=tenant_header)
        except tenant_model.DoesNotExist as e:
            msg = f"Invalid tenant: {tenant_header}"
            raise AuthenticationFailed(msg) from e
        request.tenant = tenant
        connection.set_tenant(tenant)
