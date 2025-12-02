from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View

from ticketless.dashboard.tenant.permissions import IsOwnerOrManager
from ticketless.events.mixins import JsonPermissionMixin
from ticketless.tickets.forms import EventCreationForm


class ProcessEventCreationView(
    LoginRequiredMixin, IsOwnerOrManager, JsonPermissionMixin, View
):
    permission = "tickets.add_event"
    event_create_form = EventCreationForm

    def post(self, request, *args, **kwargs):
        form = self.event_create_form(request.POST, request.FILES)
        if form.is_valid():
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
