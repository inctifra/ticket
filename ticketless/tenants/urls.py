from django.urls import include
from django.urls import path

from .views import PrivacyView
from .views import TenantHomeView

app_name = "tenants"

urlpatterns = [
    path("", TenantHomeView.as_view(), name="home"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path(
        "dashboard/", include("ticketless.dashboard.tenant.urls", namespace="dashboard")
    ),
]
