from django import forms
from django.db.models import Q
from django_select2 import forms as s2forms

from ticketless.tickets.models import Event
from ticketless.users.models import Profile


class EventWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "title__icontains",
    ]


class UserWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "user__email__icontains",
        "user__username__icontains",
    ]


class AssignScanningPermissionForm(forms.Form):
    event = forms.ModelChoiceField(
        queryset=Event.objects.none(),
        empty_label=None,
    )

    users = forms.ModelMultipleChoiceField(queryset=Profile.objects.none())

    def __init__(self, *args, **kwargs):
        self.manager = kwargs.pop("manager")
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["event"].queryset = Event.objects.filter(is_published=True)
        self.fields["users"].queryset = Profile.objects.filter(
            Q(user__is_staff=False) & Q(user__is_superuser=False)
        ).exclude(
            Q(user=self.request.user) | Q(user__email="AnonymousUser") | Q(role="S")
        )
