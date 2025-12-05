from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path("", include("ticketless.api.events.urls", namespace="api-events")),
    path(
        "tenants/",
        views.TenantListView.as_view(),
        name="api-load-tenants",
    ),
    path(
        "event-search/",
        views.EventSearchView.as_view(),
        name="api-search-events",
    ),
    path(
        "events/<slug>/",
        views.EventDetailView.as_view(),
        name="api-detail-event",
    ),
    path(
        "events-ticket/<event_slug>/scan/",
        views.ScanTicketView.as_view(),
        name="api-scan-ticket",
    ),
]
