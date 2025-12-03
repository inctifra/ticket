from django import forms

from ticketless.tickets.widgets import TicketTypeSelect

from .models import Event, TicketType


class EventCreationForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        )
    )
    end_at = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )

    class Meta:
        model = Event
        fields = [
            "title",
            "short_description",
            "start_at",
            "end_at",
            "venue_name",
            "venue_address",
            "capacity",
            "cover",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "short_description": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
            "venue_name": forms.TextInput(attrs={"class": "form-control"}),
            "venue_address": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        """Custom validation: end date must be after start date."""
        cleaned_data = super().clean()
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")

        if end_at and start_at and end_at < start_at:
            self.add_error("end_at", "End date must be after the start date.")
        return cleaned_data


class ProcessTicketCheckoutForm(forms.Form):
    ticket_type = forms.ModelChoiceField(
        queryset=TicketType.objects.none(),
        empty_label=None,
        widget=TicketTypeSelect(
            attrs={
                "class": "selectpicker w-100",
                "data-live-search": "true",
                "required": True,
            }
        ),
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control h_50", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control h_50", "placeholder": "Last Name"}
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control h_50", "placeholder": "Email Address"}
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control h_50", "placeholder": "Phone Number"}
        ),
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control h_50",
                "placeholder": "Quantity",
                "min": "1",
                "step": "1",
                "id": "ticket-qty",
            }
        ),
    )
    total_price = forms.DecimalField(widget=forms.HiddenInput())
    currency = forms.CharField(initial="KES", widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        event = kwargs.pop("event", None)
        super().__init__(*args, **kwargs)
        if event:
            qs = event.event_ticket_type.filter(is_active=True)
            self.fields["ticket_type"].queryset = qs
            price_map = {str(t.id): t.price for t in qs}
            self.fields["ticket_type"].widget.price_map = price_map
