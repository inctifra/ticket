from django.urls import path

from .views import TenantHomeView, PrivacyView

urlpatterns = [
    path("", TenantHomeView.as_view(), name="home"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]
