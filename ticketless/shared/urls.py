from django.urls import path

from .views import validate_email_address

app_name = "shared"
urlpatterns = [
    path("verify-email-address/", validate_email_address, name="verify_email"),
]
