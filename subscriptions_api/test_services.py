from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import *
from .services import *
import pytest

# Test creating a subscription


@pytest.mark.django_db
def test_create_subscription_with_null_data():
    user_id = None
    with pytest.raises(ValidationError):
        id = create_subscription(user_id)


@pytest.mark.django_db
def test_create_subscription_with_null_user_id():
    user_id = None
    subscription_months = 1
    with pytest.raises(ValidationError):
        id = create_subscription(user_id)


@pytest.mark.django_db
def test_create_subscription_with_nonexistent_user_id():
    user_id = 97
    subscription_months = 1
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id


@pytest.mark.django_db
def test_create_valid_subscription():
    user_id = 97
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id

# Test updating a subscription


@pytest.mark.django_db
def test_update_subscription_with_non_existent_user_id():
    user_id = 97
    subscription_months = 1
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_user_id = 279
    new_sub_option_id = subscription_option_id
    with pytest.raises(Subscription.DoesNotExist):
        update_subscription(new_user_id, new_sub_option_id)


@pytest.mark.django_db
def test_update_subscription_with_null_subscription_option_id():
    user_id = 97
    subscription_months = 1
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_sub_option_id = None
    with pytest.raises(SubscriptionOption.DoesNotExist):
        update_subscription(id, new_sub_option_id)


@pytest.mark.django_db
def test_update_subscription_with_non_existent_subscription_option_id():
    user_id = 97
    subscription_months = 1
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_sub_option_id = 279
    with pytest.raises(SubscriptionOption.DoesNotExist):
        update_subscription(id, new_sub_option_id)


@pytest.mark.django_db
def test_valid_subscription_update():
    user_id = 97
    subscription_months = 1
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = 84
    new_subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=new_subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    update_subscription(user_id, new_subscription_option_id)
    subscription = Subscription.objects.get(pk=id)
    sub_months = subscription.subscription_option.subscription_months
    assert sub_months == new_subscription_months

# Test getting the subscription status


@pytest.mark.django_db
def test_get_status_for_nonexistent_user_id():
    user_id = 72
    status = check_subscription(user_id)
    assert status is False


@pytest.mark.django_db
def test_get_status_where_multiple_subscriptions_exists():
    user_id = 1
    id = create_subscription(user_id)
    assert id is not None
    sub1 = Subscription.objects.get(pk=id)
    assert sub1.user_id == user_id

    id2 = create_subscription(user_id)
    assert id is not None
    sub2 = Subscription.objects.get(pk=id2)
    assert sub2.user_id == user_id

    with pytest.raises(IntegrityError):
        check_subscription(user_id)


@pytest.mark.django_db
def test_get_status_where_subscription_expired():
    user_id = 1
    subscription_months = 1
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.start_date = date(2023, 1, 1)
    assert subscription.is_active() is False


@pytest.mark.django_db
def test_get_status_where_subscription_active():
    user_id = 1
    subscription_months = 1
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id
    id = create_subscription(user_id)
    assert id is not None

    update_subscription(user_id, subscription_option_id)

    subscription = Subscription.objects.get(pk=id)
    assert subscription.is_active() is True
    sub_months = subscription.subscription_option.subscription_months
    assert sub_months == subscription_months
