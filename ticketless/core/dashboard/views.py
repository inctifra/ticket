from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ticketless.customers.models import Client
from ticketless.events.forms import EventLaunchRequestUpdateForm
from ticketless.events.models import EventLaunchRequest


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "pages/dashboard/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_requests_pending"] = EventLaunchRequest.objects.filter(
            status="P"
        )
        context["event_requests"] = EventLaunchRequest.objects.all()
        context["clients"] = Client.objects.exclude(schema_name="public")
        context["event_requests_form"] = EventLaunchRequestUpdateForm(
            manager=self.request.user.profile
        )
        return context
