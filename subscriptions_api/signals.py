"""Define signals to create and update subscriptions."""

from django.db.models.signals import post_save
from django.contrib.auth.models import User

from payments_api.models import Payment
from .models import Subscription
from .services import create_subscription, update_subscription


def trigger_subscription_creation(sender, instance, created, **kwargs):
    """Create a subscription when a user is created."""

    if created:
        create_subscription(instance.id)


def trigger_subscription_update(sender, instance, created, **kwargs):
    """Update the subscription status when a payment is completed."""

    if not created:
        if instance.status == 4:
            update_subscription(
                instance.user_id,
                instance.subscription_option_id
            )


post_save.connect(trigger_subscription_creation, sender=User)
post_save.connect(trigger_subscription_update, sender=Payment)
