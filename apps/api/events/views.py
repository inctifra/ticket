from django.http import JsonResponse
from collections import Counter

from django.shortcuts import get_object_or_404
from django.views import View

from apps.events.forms import EventLaunchRequestUpdateForm
from apps.events.models import EventLaunchRequest
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from tenant_users.tenants.tasks import provision_tenant
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


@method_decorator(login_required(login_url="/"), name="dispatch")
class AdminProcessEventRequestView(View):
    form_class = EventLaunchRequestUpdateForm

    def post(self, request, *args, **kwargs):
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

        event_request = form.save()

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
            tenant, domain = provision_tenant(
                form.cleaned_data.get("full_name"),
                form.cleaned_data.get("subdomain"),
                client,
                tenant_type="tenant_type"
            )
            with tenant_context(tenant):
                User.objects.create_user(
                    email=form.cleaned_data.get("email"),
                    password=form.cleaned_data.get("password", "phone")
                )
                client.profile.save()
        except (Exception, ValueError) as e:
            return JsonResponse({"details": str(e)}, safe=False, status=400)

        return JsonResponse(
            {"detail": f"Updated to status {event_request.get_status_display()}"},
            safe=False,
            status=200,
        )


