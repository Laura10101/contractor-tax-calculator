from django.contrib.auth.models import User

from payments_api.models import *
from payments_api.services import *

from .models import *
import pytest


@pytest.mark.django_db
def test_creating_user_also_creates_subscription():
    username = 'mytestuser'
    password = 'mytestpass'

    user = User.objects.create(username=username, password=password)

    subscriptions = Subscription.objects.filter(user_id__exact=user.id)
    assert subscriptions.count() == 1
    assert subscriptions.first().user_id == user.id


@pytest.mark.django_db
def test_completing_payment_also_updates_subscription():
    username = 'mytestuser'
    password = 'mytestpass'

    user = User.objects.create(username=username, password=password)
    subscription = Subscription.objects.filter(user_id__exact=user.id).first()

    assert not subscription.is_active()

    subscription_option = SubscriptionOption.objects.create(
        subscription_months=6,
        subscription_price=4.99,
        is_active=True
    )

    # Create a dummy payment
    payment_id, _ = create_payment(
        subscription.user_id,
        subscription_option.id,
        4.99,
        'GBP'
    )
    assert payment_id is not None

    # Complete the payment
    payment = Payment.objects.get(pk=payment_id)
    complete_payment(payment.stripe_pid)

    # Check the subscription has updated
    subscription = Subscription.objects.get(pk=subscription.id)
    assert subscription.is_active() is True
    psoid = payment.subscription_option_id
    assert subscription.subscription_option.id == psoid
