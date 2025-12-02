from django.urls import include, path
from . import views


app_name = "events"

urlpatterns = [
    # path("tickets/", include("ticketless.dashboard.tenant.events.tickets.urls")),
    path(
        "process-event-creation/",
        views.ProcessEventCreationView.as_view(),
        name="process_event_creation",
    ),
]
