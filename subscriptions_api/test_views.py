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
    subscription_months = None
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_subscription_with_null_user_id():
    user_id = None
    subscription_months = 1
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_subscription_with_nonexistent_user_id():
    user_id = 72
    subscription_months = 6
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_subscription_with_null_months():
    user_id = 1
    subscription_months = None
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_subscription_with_negative_months():
    user_id = 1
    subscription_months = -6
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_valid_subscription():
    user_id = 1
    subscription_months = 6
    body = { 'user_id': user_id, 'subscription_months': subscription_months }
    response = client.post(url, body, format='json')
    assert response is not None
    assert response.status_code == 200
    id = response.data['id']
    subscription = Subscription.objects.get(pk=id)
    assert subscription.user_id == user_id
    assert subscription.subscription_months == subscription_months

# Test updating a subscription
@pytest.mark.django_db
def test_patch_subscription_with_null_months():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = None
    body = { 'user_id': user_id, 'subscription_months': new_subscription_months }
    response = client.patch(url + '/' + str(id) + '/', body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_patch_subscription_with_negative_months():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = -6
    body = { 'user_id': user_id, 'subscription_months': new_subscription_months }
    response = client.patch(url + '/' + str(id) + '/', body, format='json')
    assert response is not None
    assert response.status_code == 400

@pytest.mark.django_db
def test_patch_subscription_update():
    user_id = 1
    subscription_months = 6
    id = create_subscription(user_id, subscription_months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)

    new_subscription_months = 1
    body = { 'user_id': user_id, 'subscription_months': new_subscription_months }
    response = client.patch(url + '/' + str(id) + '/', body, format='json')
    assert response is not None
    id = response.data['id']
    subscription = Subscription.objects.get(pk=id)
    assert subscription.subscription_months == new_subscription_months

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
    request_url = url + '/status/'
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

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    assert response is not None
    assert response.status_code == 409

@pytest.mark.django_db
def test_get_status_where_subscription_expired():
    user_id = 1
    request_url = url + '/status/'
    months = 1
    id = create_subscription(user_id, months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.start_date = date(2023, 1, 1)
    subscription.save()

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    assert response is not None
    assert response.status_code == 200
    assert response.data['status'] == False

@pytest.mark.django_db
def test_get_status_where_subscription_active():
    user_id = 1
    request_url = url + '/status/'
    months = 1
    id = create_subscription(user_id, months)
    assert id is not None
    subscription = Subscription.objects.get(pk=id)
    subscription.save()

    params = {'user_id': user_id}
    response = client.get(request_url, params)
    assert response is not None
    assert response.status_code == 200
    assert response.data['status'] == True