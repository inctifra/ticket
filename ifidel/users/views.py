from allauth.account.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from allauth.account.forms import (
    LoginForm,
)
from ifidel.users.models import User
from django.contrib.auth import login, authenticate
from django_tenants.utils import schema_context, tenant_context


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class AjaxLoginView(LoginView):
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request=request)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = User.objects.first()
        form.login()
        return JsonResponse({"success": True, "redirect_url": "/dashboard/"})


ajax_login_view = AjaxLoginView.as_view()
