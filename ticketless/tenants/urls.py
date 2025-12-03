from django.urls import include
from django.urls import path

from .views import PrivacyView
from .views import TenantHomeView, TenantEventDetailView, TenantEventCheckoutView

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
        "dashboard/", include("ticketless.dashboard.tenant.urls", namespace="dashboard")
    ),
    path("actions/", include("ticketless.tenants.actions.urls", namespace="actions")),
]
