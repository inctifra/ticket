from django.urls import path

from .views import AdminProcessEventRequestView, event_status_chart

app_name = "api-events"
urlpatterns = [
    path("event-status-chart/", event_status_chart, name="event_status_chart"),
    path(
        "request-process/<event_request_pk>/",
        AdminProcessEventRequestView.as_view(),
        name="event_request_review",
    ),
]
