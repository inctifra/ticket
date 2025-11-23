from django.urls import include
from django.urls import path

from .views import AboutView
from .views import HomeView
from .views import PrivacyView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("dashboard/", include("apps.core.dashboard.urls", namespace="dashboard")),
]
