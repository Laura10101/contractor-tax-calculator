"""Define service methods for the subscriptions API."""

from datetime import datetime
from .models import Subscription, SubscriptionOption
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def create_subscription(user_id):
    """Create a new subscription for a given user id."""
    """This will be triggered when the user is first created."""
    """The default subscription will have no option."""

    if user_id is None or user_id == '':
        raise ValidationError('A valid username must be provided')

    # Load the subscription option
    subscription_option = None
    # Create new subscription in the database
    new_subscription = Subscription.objects.create(
        user_id=user_id,
        subscription_option=subscription_option,
        start_date=datetime.now()
        )
    # Return ID of newly created jurisdiction
    return new_subscription.id


def check_subscription(user_id):
    """Check if the specified user has an active subscription."""

    print('Checking subscription for user ' + str(user_id))
    # Get the subscription from the database for the user ID
    subscriptions = Subscription.objects.filter(user_id__exact=user_id)
    print('Retrieved subscriptions for user ' + str(user_id))
    print(str(len(subscriptions)))
    print('Number of subscriptions is shown above')
    # Return an error if more than one subscription
    if len(subscriptions) > 1:
        print('More than one exception found for user ' + str(user_id))
        raise IntegrityError("More than one subscription found for user")
    # Return false if no subscription for that user ID
    if len(subscriptions) <= 0:
        print('No subscription found for user ' + str(user_id))
        return False

    print('Exactly one subscription found for user ' + str(user_id))
    # If subscription, call is_active function and return result
    return subscriptions.first().is_active()


def update_subscription(user_id, subscription_option_id):
    """Extend a subscription with the specified number of months."""

    print('User id is :' + str(user_id))
    if user_id is None or user_id == '':
        raise ValidationError('A valid username must be provided')
    # Load the subscription option
    subscription_option = SubscriptionOption.objects.get(
        pk=subscription_option_id
    )
    # Get the subscription from the database for the user ID
    subscriptions = Subscription.objects.filter(user_id__exact=int(user_id))
    # Return an error if more than one subscription
    if len(subscriptions) > 1:
        print('More than one subscription found for user ' + str(user_id))
        raise Exception("More than one subscription found for user")
    # Return false if no subscription for that user ID
    if len(subscriptions) <= 0:
        print('No subscription found for user ' + str(user_id))
        raise Subscription.DoesNotExist()
    # Patch start date
    subscription = subscriptions.first()
    subscription.start_date = datetime.now()
    # Patch subscription months
    subscription.subscription_option = subscription_option
    subscription.save()


def get_subscription_options():
    """Get a list of all subscription options."""
    return SubscriptionOption.objects.all()


def get_subscription_option(id):
    """Get the details of a specific subscription option."""
    return SubscriptionOption.objects.get(pk=id)
