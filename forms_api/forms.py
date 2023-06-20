from django import forms
from dal import autocomplete

from .models import Form

class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        widgets = {
            'jurisdiction_id': autocomplete.ListSelect2('jurisdiction-autocomplete')
        }
        exclude = []

