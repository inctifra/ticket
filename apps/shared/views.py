from django.shortcuts import render
from django.views.generic import TemplateView


class PrivacyView(TemplateView):
    template_name = "shared/pages/privacy.html"
