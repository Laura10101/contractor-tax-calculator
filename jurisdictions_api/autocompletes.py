"""Define autocompletes for the jurisdiction model."""

from dal import autocomplete

from .models import Jurisdiction


class JurisdictionAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete for the jurisdiction model."""

    def get_queryset(self):
        """Return data to populate the autocomplete."""

        return Jurisdiction.objects.all()
