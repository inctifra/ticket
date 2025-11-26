from django.views.generic import TemplateView

from apps.plan.models import Plan
from apps.tenants.middleware import get_current_user
from apps.tenants.models import Client


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenants"] = Client.objects.exclude(
            schema_name=self.request.tenant.schema_name
        )
        context["plans"] = Plan.objects.all()
        print("User", get_current_user())
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"


class PrivacyView(TemplateView):
    template_name = "pages/privacy.html"
