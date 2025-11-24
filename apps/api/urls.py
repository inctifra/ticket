from django.urls import path, include


urlpatterns = [path("", include("apps.api.events.urls", namespace="api-events"))]
