from django.apps import apps
from django.http import JsonResponse


class JsonPermissionMixin:
    permission: str = ""

    def dispatch(self, request, *args, **kwargs):
        perm = self.permission
        if perm and not request.user.has_perm(perm):
            return JsonResponse(
                {"success": False, "error": self.build_perm_message(perm)}, status=403
            )
        return super().dispatch(request, *args, **kwargs)

    def build_perm_message(self, perm):
        app_label, codename = perm.split(".")
        action, model_part = codename.split("_", 1)
        model = apps.get_model(app_label, model_part)
        return f"You do not have permission to {action} {model._meta.verbose_name}."  # noqa: SLF001


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(form.errors, status=400)
        return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # save the object).
        response = super().form_valid(form)
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = {
                "pk": self.object.pk,
            }
            return JsonResponse(data)
        return response
