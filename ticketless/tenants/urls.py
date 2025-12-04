from django.urls import include
from django.urls import path

from .views import PrivacyView
from .views import TenantEventCheckoutView
from .views import TenantEventDetailView
from .views import TenantHomeView
from .views import TenantTicketDownloadTicketView

app_name = "tenants"

urlpatterns = [
    path("", TenantHomeView.as_view(), name="home"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("events/<slug:slug>/", TenantEventDetailView.as_view(), name="event_detail"),
    path(
        "events/<slug:slug>/checkout/",
        TenantEventCheckoutView.as_view(),
        name="event_ticket_checkout",
    ),
    path(
        "events/tickets/download/<order_item_id>/",
        TenantTicketDownloadTicketView.as_view(),
        name="download_ticket_view",
    ),
    path(
        "dashboard/", include("ticketless.dashboard.tenant.urls", namespace="dashboard")
    ),
    path("actions/", include("ticketless.tenants.actions.urls", namespace="actions")),
]
