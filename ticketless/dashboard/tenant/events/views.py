from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from ticketless.dashboard.tenant.permissions import IsOwnerOrManager
from ticketless.tickets.forms import EventCreationForm


# @method_decorator(
#     permission_required("tickets.add_event", raise_exception=True), name="dispatch"
# )
class ProcessEventCreationView(LoginRequiredMixin, IsOwnerOrManager, View):
    event_create_form = EventCreationForm

    def post(self, request, *args, **kwargs):
        form = self.event_create_form(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid", form.cleaned_data)
            return JsonResponse(
                {"success": True, "message": "Event created successfully."}
            )
        return JsonResponse({"success": False, "errors": form.errors}, status=400)
