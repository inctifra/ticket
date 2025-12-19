from django.urls import path

from .views import TenantAPIListView


app_name = "api-tenants"

urlpatterns = [
    path("", TenantAPIListView.as_view()),
]
