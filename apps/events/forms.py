from django import forms

from apps.plan.models import Plan
from .models import EventLaunchRequest, EVENT_TYPES


class EventLaunchRequestForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Plan"
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
            "email": "We’ll send onboarding instructions here.",
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
