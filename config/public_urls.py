from django.contrib import admin
from django.urls import include
from django.urls import path

from .shared_urls import shared_urlpatterns

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.shared.urls", namespace="shared")),
]
urlpatterns += [*shared_urlpatterns]

admin.site.site_header = "Ticketless Admin Panel"
admin.site.site_title = "Ticketless - Event Management"
admin.site.index_title = "Dashboard Overview"
