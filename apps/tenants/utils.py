from django.contrib.auth import get_user_model
from django_tenants.utils import tenant_context
from config.settings.base import env

User = get_user_model()
password = env.str("TENANT_SUPERUSER_PASSWORD")

def create_tenant_superuser(tenant, email, password=password):
    """
    Creates a superuser directly inside the tenant schema programmatically.
    """

    with tenant_context(tenant):
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email,
                password=password
            )
