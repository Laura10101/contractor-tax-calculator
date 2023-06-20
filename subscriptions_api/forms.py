from django import forms
from dal import autocomplete

from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        widgets = {
            'user_id': autocomplete.ListSelect2('user-autocomplete'),
        }
        exclude = []