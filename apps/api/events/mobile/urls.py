from django.urls import path

from .views import EventSearchAPIView

app_name = "mobile"
urlpatterns = [path("events-search/", EventSearchAPIView.as_view())]
