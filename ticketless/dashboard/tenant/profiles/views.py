from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView

from ticketless.dashboard.tenant.forms import AssignScanningPermissionForm
from ticketless.dashboard.tenant.permissions import IsOwnerOrManager
from ticketless.users.models import Profile


class ProfileView(LoginRequiredMixin, IsOwnerOrManager, TemplateView):
    template_name = "tenants/dashboard/profiles/index.html"
    scanning_form_class = AssignScanningPermissionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles_requests"] = Profile.objects.filter(
            Q(user__is_staff=False) & Q(user__is_superuser=False)
        ).exclude(Q(user=self.request.user) | Q(user__email="AnonymousUser"))
        context["assign_scanning_permission_form"] = AssignScanningPermissionForm(
            manager=self.request.user, request=self.request
        )
        return context
