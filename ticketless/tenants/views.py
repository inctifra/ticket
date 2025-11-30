from django.views.generic import TemplateView


class TenantHomeView(TemplateView):
    template_name = "tenants/pages/home.html"


class PrivacyView(TemplateView):
    template_name = "tenants/pages/privacy.html"
