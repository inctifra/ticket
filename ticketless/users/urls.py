from django.urls import path

from .views import ajax_login_view
from .views import dynamic_login_redirect
from .views import user_detail_view
from .views import user_redirect_view
from .views import user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path("ajax/login/", view=ajax_login_view, name="ajax_login"),
    path(
        "redirect-after-login/", dynamic_login_redirect, name="dynamic-login-redirect"
    ),
]
