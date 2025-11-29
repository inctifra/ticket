# from django.contrib.auth import get_user_model
# from django_tenants.utils import tenant_context
# from .models import Client, Domain

# User = get_user_model()

# def create_tenant(
#     schema_name: str,
#     tenant_name: str,
#     domain_url: str,
#     description: str = "",
#     owner=None,
#     manager=None,
# ):
#     """
#     Programmatically create a tenant, its domain, and a tenant superuser.
#     """

#     # 1️⃣ Create tenant
#     tenant = Client.objects.create(
#         schema_name=schema_name,
#         name=tenant_name,
#         description=description,
#         owner=owner,
#         manager=manager,
#     )
#     # auto_create_schema = True will run migrations here

#     # 2️⃣ Create domain for this tenant
#     Domain.objects.create(
#         domain=domain_url,
#         tenant=tenant,
#         is_primary=True,
#     )

#     # 3️⃣ Create superuser inside tenant schema
#     with tenant_context(tenant):
#         if superuser_email is None:
#             superuser_email = f"{superuser_username}@{schema_name}.tenant"

#         if not User.objects.filter(username=superuser_username).exists():
#             User.objects.create_superuser(
#                 username=superuser_username,
#                 email=superuser_email,
#                 password=superuser_password,
#             )

#     return tenant
