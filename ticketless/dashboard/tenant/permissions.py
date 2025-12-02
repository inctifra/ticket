from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


def is_owner_or_manager(u):
    return (
        hasattr(u, "tenant")
        or (u.owned_tenants.exists() or u.managed_tenants.exists())
        or u.is_superuser
    )


class IsOwnerOrManager(UserPassesTestMixin):
    """
    Custom permission to only allow owners or managers of a
    tenant to access certain views.
    """

    def test_func(self):
        return is_owner_or_manager(self.request.user)

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = "You do not have permission to access the tenant dashboard."
            raise PermissionDenied(message)

        return super().handle_no_permission()
