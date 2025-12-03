from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketless.tickets.models import Event


class TenantHomeView(TemplateView):
    template_name = "tenants/pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all().order_by("-created_at")
        return context


class TenantEventDetailView(TemplateView):
    template_name = "tenants/pages/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = get_object_or_404(Event, slug=self.kwargs.get("slug"))
        context["events"] = Event.objects.all().order_by("-created_at")
        return context


class PrivacyView(TemplateView):
    template_name = "tenants/pages/privacy.html"
