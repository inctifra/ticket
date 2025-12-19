from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.tenants.permissions import owner_or_manager_required


@method_decorator([login_required, owner_or_manager_required], name="dispatch")
class HomeView(TemplateView):
    template_name = "tenants/dashboard/pages/home.html"
