from django.urls import path

from .views import EventLaunchRequestView

urlpatterns = [
    path("launch/", EventLaunchRequestView.as_view(), name="launch_view")
]

