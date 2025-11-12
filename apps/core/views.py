from django.views.generic import TemplateView

from apps.tenants.models import Client


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tenants"] = Client.objects.exclude(
            schema_name=self.request.tenant.schema_name
        )
        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"
