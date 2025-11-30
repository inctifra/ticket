from django.urls import path

from ticketless.shared.views import validate_email_address

from .views import EventLaunchRequestView

app_name = "events"

urlpatterns = [
    path("launch/", EventLaunchRequestView.as_view(), name="launch_view"),
    path("verify-email-address/", validate_email_address, name="verify_email"),
]
