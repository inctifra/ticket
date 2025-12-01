from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from django.contrib import messages


def is_owner_or_manager(user):
    return user.owned_tenants.exists() or user.managed_tenants.exists()


class HomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "tenants/dashboard/pages/home.html"

    def test_func(self):
        u = self.request.user
        return (
            hasattr(u, "tenant")
            or (u.owned_tenants.exists() or u.managed_tenants.exists())
            or u.is_superuser
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            message = "You do not have permission to access the tenant dashboard."
            raise PermissionDenied(message)

        return super().handle_no_permission()


home = HomeView.as_view()
