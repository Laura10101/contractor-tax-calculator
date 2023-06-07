from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

# Test creating a subscription
@pytest.mark.django_db
def test_create_subscription_with_null_data():
    user_id = None
    subscription_months = None
    with pytest.raises(IntegrityError):
        id = create_subscription(user_id, subscription_months)

@pytest.mark.django_db
def test_create_subscription_with_null_user_id():
    user_id = None
    subscription_months = 1
    with pytest.raises(IntegrityError):
        id = create_subscription(user_id, subscription_months)

@pytest.mark.django_db
def test_create_subscription_with_nonexistent_user_id():
    user_id = 72
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id
    assert subscription.subscription_months == subscription_months

@pytest.mark.django_db
def test_create_subscription_with_null_months():
    user_id = 1
    subscription_months = None
    with pytest.raises(IntegrityError):
        id = create_subscription(user_id, subscription_months)

@pytest.mark.django_db
def test_create_subscription_with_negative_months():
    user_id = 1
    subscription_months = -6
    with pytest.raises(ValidationError):
        id = create_subscription(user_id, subscription_months)

@pytest.mark.django_db
def test_create_valid_subscription():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id
    assert subscription.subscription_months == subscription_months

# Test updating a subscription
@pytest.mark.django_db
def test_update_subscription_with_null_months():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = None
    with pytest.raises(IntegrityError):
        update_subscription(id, new_subscription_months)

@pytest.mark.django_db
def test_update_subscription_with_negative_months():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = -6
    with pytest.raises(ValidationError):
        update_subscription(id, new_subscription_months)

@pytest.mark.django_db
def test_valid_subscription_update():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = 1
    update_subscription(id, new_subscription_months)
    subscription = Subscription.objects.get(pk=id)
    assert subscription.subscription_months == new_subscription_months

# Test getting the subscription status
@pytest.mark.django_db
def test_get_status_for_nonexistent_user_id():
    user_id = 72
    status = check_subscription(user_id)
    assert status == False

@pytest.mark.django_db
def test_get_status_where_multiple_subscriptions_exists():
    user_id = 1
    id1 = create_subscription(user_id, 6)
    assert id is not None
    sub1 = Subscription.objects.get(pk=id1)
    assert sub1.user_id == user_id
    assert sub1.subscription_months == 6

    id2 = create_subscription(user_id, 3)
    assert id is not None
    sub2 = Subscription.objects.get(pk=id2)
    assert sub2.user_id == user_id
    assert sub2.subscription_months == 3

    with pytest.raises(Exception):
        check_subscription(user_id)

@pytest.mark.django_db
def test_get_status_where_subscription_expired():
    user_id = 1
    months = 1
    id = create_subscription(user_id, months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.start_date = date(2023, 1, 1)
    assert subscription.is_active() == False

@pytest.mark.django_db
def test_get_status_where_subscription_active():
    user_id = 1
    months = 1
    id = create_subscription(user_id, months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    assert subscription.is_active() == True