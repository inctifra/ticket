from django.http import HttpRequest, JsonResponse
from collections import Counter

from django.shortcuts import get_object_or_404
from django.views import View

from apps.events.forms import EventLaunchRequestUpdateForm
from apps.events.models import EventLaunchRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.tenants.models import Client, Domain
from ifidel.users.models import User
from django_tenants.utils import tenant_context


def event_status_chart(request):
    all_requests = EventLaunchRequest.objects.all()
    status_counts = Counter(all_requests.values_list("status", flat=True))
    chart_labels = []
    chart_data = []

    for code, label in EventLaunchRequest.STATUS_CHOICES:
        chart_labels.append(label)
        chart_data.append(status_counts.get(code, 0))

    return JsonResponse({"labels": chart_labels, "data": chart_data})


@method_decorator(login_required, name="dispatch")
class AdminProcessEventRequestView(View):
    form_class = EventLaunchRequestUpdateForm

    def post(self, request: HttpRequest, *args, **kwargs):
        event_request = get_object_or_404(
            EventLaunchRequest,
            id=kwargs.get("event_request_pk"),
        )

        form = self.form_class(
            request.POST,
            instance=event_request,
            manager=request.user.profile,
        )

        if not form.is_valid():
            return JsonResponse(form.errors, safe=False, status=400)

        event_request: EventLaunchRequest = form.save()

        client, created = User.objects.get_or_create(
            email=form.cleaned_data.get("email"),
            defaults={"name": form.cleaned_data.get("full_name")},
        )

        if created:
            client.set_password(form.cleaned_data.get("password", "phone"))
            client.save()
        if not event_request.managed_by:
            event_request.managed_by = request.user.profile
            event_request.save()
        try:
            tenant = Client(
                name=event_request.full_name,
                schema_name=event_request.subdomain,
                manager=event_request.managed_by.user,
                owner=client,
            )
            tenant.save()
            domain = Domain()
            domain.tenant = tenant
            domain.domain = f"{tenant.schema_name}.localhost"
            domain.is_primary = True
            domain.save()

        except (Exception, ValueError) as e:
            return JsonResponse({"details": str(e)}, safe=False, status=400)
        return JsonResponse(
            {"detail": f"Updated to status {event_request.get_status_display()}"},
            safe=False,
            status=200,
        )
