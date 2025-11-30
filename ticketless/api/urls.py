from django.urls import include
from django.urls import path

urlpatterns = [path("", include("ticketless.api.events.urls", namespace="api-events"))]
