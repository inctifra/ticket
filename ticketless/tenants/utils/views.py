from django.shortcuts import render
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
)


def error_403(request, exception=None):
    return HttpResponseForbidden(
        render(request, "tenants/errors/403.html", {"message": str(exception)})
    )


def error_404(request, exception=None):
    return HttpResponseNotFound(render(request, "tenants/errors/404.html"))


def error_500(request):
    return HttpResponseServerError(render(request, "tenants/errors/500.html"))
