from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.events.forms import EventLaunchRequestUpdateForm
from apps.events.models import EventLaunchRequest
from apps.tenants.models import Client


@method_decorator(login_required(login_url="/"), name="dispatch")
class HomeView(TemplateView):
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
