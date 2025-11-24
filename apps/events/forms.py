from django import forms
from django.urls import reverse
import re
from apps.plan.models import Plan

from .models import EVENT_TYPES
from .models import EventLaunchRequest

RESERVED_SUBDOMAINS = {
    "www", "admin", "api", "mail", "support", "test", "events", "ticketless"
}


MINIMUM_SUBDOMAIN_LENGTH=3

class EventLaunchRequestForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Plan",
    )

    class Meta:
        model = EventLaunchRequest
        fields = [
            "full_name",
            "email",
            "phone",
            "subdomain",
            "event_type",
            "plan",
            "event_details",
        ]
        help_texts = {
            "full_name": "Tell us who to contact.",
            "email": "We'll send onboarding instructions here.",
            "phone": "For direct communication & support.",
            "subdomain": "This will be your event portal URL.",
            "event_type": "Helps us prepare the right modules.",
            "event_details": "Share anything that helps us understand your needs.",
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "John Doe",
                    "required": True,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "you@email.com",
                    "required": True,
                    "data-verification-url": "/events/verify-email-address/",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+254 712 345 678",
                    "required": True,
                }
            ),
            "subdomain": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "tim", "required": True}
            ),
            "event_type": forms.Select(
                attrs={"class": "form-control", "required": True}, choices=EVENT_TYPES
            ),
            "event_details": forms.Textarea(
                attrs={
                    "class": "form-control p-0",
                    "rows": 4,
                    "placeholder": (
                        "Briefly describe your event, goals, expected audience...",
                    ),
                }
            ),
        }

    def clean_subdomain(self):
        subdomain = self.cleaned_data["subdomain"].lower().strip()

        if not re.match(r"^[a-z0-9-]+$", subdomain):
            msg = "Subdomain can only contain letters, numbers, and hyphens."
            raise forms.ValidationError(
                msg
            )

        if not re.match(r"^[a-z0-9].*[a-z0-9]$", subdomain):
            msg = "Subdomain must start and end with a letter or number."
            raise forms.ValidationError(msg)

        if len(subdomain) < MINIMUM_SUBDOMAIN_LENGTH:
            msg = "Subdomain must be at least 3 characters long."
            raise forms.ValidationError(msg)

        if subdomain in RESERVED_SUBDOMAINS:
            msg = f"'{subdomain}' is reserved and cannot be used as a subdomain."
            raise forms.ValidationError(msg)

        if EventLaunchRequest.objects.filter(subdomain=subdomain).exists():
            msg = "This subdomain is already taken."
            raise forms.ValidationError(msg)

        return subdomain
