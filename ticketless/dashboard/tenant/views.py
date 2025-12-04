from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ticketless.dashboard.tenant.permissions import IsOwnerOrManager
from ticketless.tickets.forms import EventCreationForm
from ticketless.tickets.models import Event


class HomeView(LoginRequiredMixin, IsOwnerOrManager, TemplateView):
    template_name = "tenants/dashboard/pages/home.html"
    event_create_form = EventCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_create_form"] = self.event_create_form()
        context["events"] = Event.objects.all().order_by("-created_at")
        return context


home = HomeView.as_view()
