from django import forms
from dal import autocomplete

from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        widgets = {
            'subscription_id': autocomplete.ListSelect2('subscription-autocomplete'),
            'subscription_option_id': autocomplete.ListSelect2('subscription-option-autocomplete'),
        }
        exclude = []