from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path(
        "process-event-creation/",
        views.ProcessEventCreationView.as_view(),
        name="process_event_creation",
    ),
]
