from django.db import connection
from django.http import Http404, JsonResponse
from apps.tenants.models import Client


class SafeTenantAccessMiddleware:
    EXEMPT_PATHS = (
        "/__reload__/",
        "/static/",
        "/media/",
        "/favicon.ico",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for path in self.EXEMPT_PATHS:
            if request.path.startswith(path):
                return self.get_response(request)

        if not hasattr(request, "tenant"):
            return self.get_response(request)

        return self.get_response(request)
