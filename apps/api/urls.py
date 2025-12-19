from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("apps.api.events.urls", namespace="api-events")),
    path("tenants/", include("apps.api.tenants.urls", namespace="api-tenants")),
]
