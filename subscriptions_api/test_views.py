from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

client = APIClient()
url = '/api/subscriptions/'

# Test creating a subscription


@pytest.mark.django_db
def test_post_subscription_with_null_data():
    user_id = None

    body = {
        'user_id': user_id
    }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_subscription_with_null_user_id():
    user_id = None

    body = {
        'user_id': user_id
    }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_subscription_with_nonexistent_user_id():
    user_id = 72

    body = {
        'user_id': user_id
    }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_valid_subscription():
    user_id = 1

    body = {
        'user_id': user_id
    }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 200
    id = response.data['subscription_id']
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id

# Test updating a subscription


@pytest.mark.django_db
def test_patch_subscription_with_null_subscription_option_id():
    user_id = 1
    subscription_months = 6
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id

    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    body = {
        'user_id': user_id,
        'subscription_option_id': None
    }
    response = client.patch(url, body, format='json')
    assert response is not None
    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_subscription():
    user_id = 1
    subscription_months = 6
    subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id

    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = 1
    new_subscription_option_id = SubscriptionOption.objects.create(
        subscription_months=new_subscription_months,
        subscription_price=9.99,
        is_active=True
    ).id

    body = {
        'user_id': user_id,
        'subscription_option_id': new_subscription_option_id
    }
    response = client.patch(url, body, format='json')
    print(response.data)
    assert response is not None
    assert response.status_code == 200
    subscription = Subscription.objects.get(user_id__exact=id)
    sub_months = subscription.subscription_option.subscription_months
    assert sub_months == new_subscription_months

# Test getting the subscription status


@pytest.mark.django_db
def test_get_status_for_nonexistent_user_id():
    user_id = 72
    request_url = url + '/status/'
    params = {'user_id': user_id}
    response = client.get(request_url, params)
    assert response is not None
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_status_where_multiple_subscriptions_exists():
    user_id = 1
    request_url = url + 'status/'

    id1 = create_subscription(user_id)
    assert id is not None
    sub1 = Subscription.objects.get(pk=id1)
    assert sub1.user_id == user_id

    id2 = create_subscription(user_id)
    assert id is not None
    sub2 = Subscription.objects.get(pk=id2)
    assert sub2.user_id == user_id

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    assert response is not None
    assert response.status_code == 409


@pytest.mark.django_db
def test_get_status_where_subscription_expired():
    user_id = 1
    request_url = url + 'status/'
    months = 1
    subscription_option = SubscriptionOption.objects.create(
        subscription_months=months,
        subscription_price=9.99,
        is_active=True
    )
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.start_date = date(2023, 1, 1)
    subscription.subscription_option = subscription_option
    subscription.save()

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    print(response.data)
    assert response is not None
    assert response.status_code == 200
    assert response.data['has_active_subscription'] is False


@pytest.mark.django_db
def test_get_status_where_subscription_active():
    user_id = 1
    request_url = url + 'status/'
    print(request_url)
    months = 1
    subscription_option = SubscriptionOption.objects.create(
        subscription_months=months,
        subscription_price=9.99,
        is_active=True
    )
    id = create_subscription(user_id)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.subscription_option = subscription_option
    subscription.save()

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    print(response.data)
    assert response is not None
    assert response.status_code == 200
    assert response.data['has_active_subscription'] is True
