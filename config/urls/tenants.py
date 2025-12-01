from django.urls import include
from django.urls import path

from .base import urlpatterns as base_urlpatterns

urlpatterns = [
    path("", include("ticketless.tenants.urls", namespace="tenants")),
    *base_urlpatterns,
]

handler403 = "ticketless.tenants.utils.views.error_403"
handler404 = "ticketless.tenants.utils.views.error_404"
handler500 = "ticketless.tenants.utils.views.error_500"
