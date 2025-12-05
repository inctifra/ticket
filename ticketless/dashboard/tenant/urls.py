from django.urls import include
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "events/",
        include("ticketless.dashboard.tenant.events.urls", namespace="events"),
    ),
    path(
        "profiles/",
        include("ticketless.dashboard.tenant.profiles.urls", namespace="profiles"),
    ),
]
