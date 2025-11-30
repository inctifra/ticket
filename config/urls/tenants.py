from django.urls import include
from django.urls import path

from .base import urlpatterns as base_urlpatterns

urlpatterns = [
    path("", include("ticketless.tenants.urls", namespace="tenants")),
    *base_urlpatterns,
]
