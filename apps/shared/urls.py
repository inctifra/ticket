from django.urls import path

from .views import PrivacyView
app_name = "shared"
urlpatterns = [
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]
