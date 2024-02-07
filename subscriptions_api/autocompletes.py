"""Define autocompletes for the subscription models model."""
from dal import autocomplete
from django.contrib.auth.models import User
from .models import Subscription, SubscriptionOption


class SubscriptionOptionAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete for the subscription option model."""

    def get_queryset(self):
        """Return data to populate the autocomplete."""

        return SubscriptionOption.objects.all()


class SubscriptionAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete for the subscription model."""

    def get_queryset(self):
        """Return data to populate the autocomplete."""

        return Subscription.objects.all()


class UserAutocomplete(autocomplete.Select2QuerySetView):
    """Autocomplete for the user model."""

    def get_queryset(self):
        """Return data to populate the autocomplete."""

        return User.objects.all()
