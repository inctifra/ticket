from django.urls import include
from django.urls import path

from .views import PrivacyView
from .views import TenantHomeView, TenantEventDetailView

app_name = "tenants"

urlpatterns = [
    path("", TenantHomeView.as_view(), name="home"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("events/<slug:slug>/", TenantEventDetailView.as_view(), name="event_detail"),
    path(
        "dashboard/", include("ticketless.dashboard.tenant.urls", namespace="dashboard")
    ),
]
