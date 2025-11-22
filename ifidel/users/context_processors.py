from django.conf import settings
from allauth.account.forms import LoginForm

def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
        "login_form": LoginForm()
    }
