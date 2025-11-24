from django.http import JsonResponse
from django.views import View

from apps.events.forms import EventLaunchRequestForm


class EventLaunchRequestView(View):
    form_class = EventLaunchRequestForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return JsonResponse(
                {"detail": "Request submitted successfully. Will contact you soon"},
                status=201,
                safe=False,
            )
        return JsonResponse({"errors": form.errors}, status=400)

