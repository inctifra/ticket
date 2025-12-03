from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ticketless.tickets.forms import ProcessTicketCheckoutForm
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


class TenantEventCheckoutView(TemplateView):
    template_name = "tenants/pages/event_ticket_checkout.html"
    ticket_checkout_form_class = ProcessTicketCheckoutForm

    def _get_event(self):
        return get_object_or_404(Event, slug=self.kwargs.get("slug"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self._get_event()
        context["ticket_purchase_form"] = self.ticket_checkout_form_class(
            event=self._get_event()
        )
        return context


class PrivacyView(TemplateView):
    template_name = "tenants/pages/privacy.html"
