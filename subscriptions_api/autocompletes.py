from dal import autocomplete
from django.contrib.auth.models import User
from .models import Subscription, SubscriptionOption

class SubscriptionOptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return SubscriptionOption.objects.all()

class SubscriptionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return Subscription.objects.all()

class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        return User.objects.all()