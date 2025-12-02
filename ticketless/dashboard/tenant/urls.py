from django.urls import include, path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "events/",
        include("ticketless.dashboard.tenant.events.urls", namespace="events"),
    ),
]
