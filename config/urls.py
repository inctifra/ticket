from django.urls import include
from django.urls import path
from .shared_urls import shared_urlpatterns
from django.contrib import admin


urlpatterns = [path("", include("apps.tenants.urls"))]
urlpatterns += [*shared_urlpatterns]

admin.site.site_header = "Ticketless Tenant Panel"
admin.site.site_title = "Ticketless - Event Management (Tenant)"
admin.site.index_title = "Dashboard Overview (Tenant)"
