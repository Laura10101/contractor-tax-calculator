from django import forms
from dal import autocomplete

from .models import RuleSet

class RuleSetForm(forms.ModelForm):
    class Meta:
        model = RuleSet
        widgets = {
            'jurisdiction_id': autocomplete.ListSelect2('jurisdiction-autocomplete')
        }
        exclude = []


    