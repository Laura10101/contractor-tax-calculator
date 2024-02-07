"""Form for the subscription model."""
from django import forms
from dal import autocomplete

from .models import Subscription


class SubscriptionForm(forms.ModelForm):
    """Form configuration for the subscription model."""

    class Meta:
        """Metadata for the subscription model form."""
        model = Subscription
        widgets = {
            'user_id': autocomplete.ListSelect2('user-autocomplete'),
        }
        exclude = []
