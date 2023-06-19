from dal import autocomplete

from .models import Jurisdiction


class JurisdictionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return Jurisdiction.objects.all()