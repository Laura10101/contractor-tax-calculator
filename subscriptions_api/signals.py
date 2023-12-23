from django.db.models.signals import post_save
from django.contrib.auth.models import User

from payments_api.models import Payment
from .models import Subscription
from .services import create_subscription, update_subscription

def trigger_subscription_creation(sender, instance, created, **kwargs):
    if created:
        create_subscription(instance.id, None)

def trigger_subscription_update(sender, instance, created, **kwargs):
    if not created:
        print('Payment updated, not created')
        print(str(instance.status))
        if instance.status == 4:
            subscription = Subscription.objects.get(pk=instance.subscription_id)
            update_subscription(subscription.user_id, instance.subscription_option_id)

post_save.connect(trigger_subscription_creation, sender=User)
post_save.connect(trigger_subscription_update, sender=Payment)