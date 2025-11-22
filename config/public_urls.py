from django.urls import include
from django.urls import path
from .shared_urls import shared_urlpatterns
from django.contrib import admin


urlpatterns = [
    path("", include("apps.core.urls")),
]
urlpatterns += [*shared_urlpatterns]

admin.site.site_header = "Ticketless Admin Panel"
admin.site.site_title = "Ticketless - Event Management"
admin.site.index_title = "Dashboard Overview"
