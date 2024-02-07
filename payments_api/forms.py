"""Define admin form for the payment model."""
from django import forms
from dal import autocomplete

from .models import Payment


class PaymentForm(forms.ModelForm):
    """Configuration for the Payment model admin form."""

    class Meta:
        """Configuration for the Payment model admin form metadata."""

        model = Payment
        widgets = {
            'subscription_id': autocomplete.ListSelect2(
                'subscription-autocomplete'
            ),
            'subscription_option_id': autocomplete.ListSelect2(
                subscription-option-autocomplete'
            ),
        }
        exclude = []
