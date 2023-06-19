from selectable.base import ModelLookup
from selectable.registry import registry

from .models import Subscription, SubscriptionOption

class SubscriptionLookup(ModelLookup):
    model = Subscription
    search_fields = ('user_id__icontains', )

class SubscriptionOptionLookup(ModelLookup):
    model = SubscriptionOption
    search_fields = ('subscription_months__icontains', )

registry.register(SubscriptionLookup)
registry.register(SubscriptionOptionLookup)