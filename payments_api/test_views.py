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

from subscriptions_api.models import Subscription, SubscriptionOption

client = APIClient()
url = '/api/payments/'

# Test creating a subscription
# Helper functions

def create_mock_subscription_option():
    return SubscriptionOption.objects.create(
        subscription_months=1,
        subscription_price=4.99,
        is_active=True
    )

def create_mock_subscription(subscription_option):
    return Subscription.objects.create(
        subscription_option = subscription_option,
        user_id = 479,
        start_date = datetime.now()
    )

# Test creating a payment
# Format for POST payload on payments API
# {
#   'subscription_id': x,
#   'subscription_option_id': x,
#   'total': x.y,
#   'currency': 'ZZZ'
# }
@pytest.mark.django_db
def test_post_payment_with_null_data():
    subscription_id = None
    subscription_option_id = None
    total = None
    currency = None

    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_payment_with_null_subscription_id():
    subscription_id = None
    subscription_option_id = create_mock_subscription_option().id.id
    total = 42.30
    currency = 'GBP'

    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_payment_with_null_subscription_option_id():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = None
    total = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_post_payment_with_negative_subscription_option_id():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = -6
    total = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_payment_with_null_total():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = None
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_payment_with_negative_total():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = -42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_payment_with_invalid_currency_code():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'G'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_post_valid_payment():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    id = response.data['payment_id']

    assert id is not None
    payment = Payment.objects.get(pk=id)
    assert payment.subscription_id == subscription_id
    assert payment.subscription_option_id == subscription_option_id
    assert payment.total == total
    assert payment.vat == (total * 0.19)
    assert payment.total == payment.total + payment.vat
    assert payment.currency == currency
    assert payment.status == 1
    assert payment.created_date == date.today()
    assert payment.intended_date == date.today()
    assert payment.stripe_pid is not None

# Test patching a payment with payment details
# Expected payload for patching payments:
# {
#   'billing_address': {
#       'street_address_1': x,
#       'street_address_2': x,
#       'city': x,
#       'county': x,
#       'country': x,
#       'postcode': x
#   },
#   'payment_details': {
#       'card_number': x,
#       'expiry_date': x,
#       'ccv2': x
#   }
# }
@pytest.mark.django_db
def test_patch_payment_with_null_payment_data():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    
    data = {
        'stripe_card_id': None
    }
    response = client.patch(url + str(None) + '/', data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_patch_payment_with_null_payment_id():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    
    data = {
        'stripe_card_id': 'pm_card_gb'
    }
    response = client.patch(url + str(None) + '/', data, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_patch_payment_with_null_stripe_card_id():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    
    data = {
        'stripe_card_id': None
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_patch_payment_with_non_string_stripe_card_id():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    
    data = {
        'stripe_card_id': 1234
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_patch_valid_payment():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    
    data = {
        'stripe_card_id': 'pm_card_gb'
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 200
    assert response.data is not None

    assert response.data['succeeded']

    payment = Payment.objects.get(pk=id)
    assert payment.status == 3
    assert payment.stripe_error is None
    assert payment.stripe_pid is not None

# Test posting the payment result
# Expected payload for Stripe webhook will be a payment intent object
# wrapped in an event object
# Event objects: https://stripe.com/docs/api/events/object
# Payment intent objects: https://stripe.com/docs/api/payment_intents

webhook_payload = {
    "id": "evt_1NGObyFkVBiDxSnkSOAnG6mj",
    "object": "event",
    "api_version": None,
    "created": 1686152966,
    "data": {
        "object": {
            "id": "pi_1JKS5I2x6R10KRrhk9GzY4BM",
            "object": "payment_intent",
            "amount": 1000,
            "amount_capturable": 0,
            "amount_details": {
                "tip": {}
            },
            "amount_received": 0,
            "application": None,
            "application_fee_amount": None,
            "automatic_payment_methods": None,
            "canceled_at": None,
            "cancellation_reason": None,
            "capture_method": "automatic",
            "client_secret": "pi_1JKS5I2x6R10KRrhk9GzY4BM_secret_N1kiKaTvicujcDGMskLXGasty",
            "confirmation_method": "automatic",
            "created": 1628014284,
            "currency": "usd",
            "customer": None,
            "description": "Created by stripe.com/docs demo",
            "invoice": None,
            "last_payment_error": None,
            "latest_charge": None,
            "livemode": False,
            "metadata": {},
            "next_action": None,
            "on_behalf_of": None,
            "payment_method": None,
            "payment_method_options": {
                "card": {
                    "installments": None,
                    "mandate_options": None,
                    "network": None,
                    "request_three_d_secure": "automatic"
                }
            },
            "payment_method_types": [
                "card"
            ],
            "processing": None,
            "receipt_email": None,
            "review": None,
            "setup_future_usage": None,
            "shipping": None,
            "statement_descriptor": None,
            "statement_descriptor_suffix": None,
            "status": "requires_payment_method",
            "transfer_data": None,
            "transfer_group": None
        }
    },
    "livemode": False,
    "pending_webhooks": 0,
    "request": {
        "id": None,
        "idempotency_key": None
    },
    "type": ""
}

@pytest.mark.django_db
def test_process_payment_success_webhook():
    client = APIClient()

    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    request_url = url + 'webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment.status == 4

    subs_id = payment.subscription_id

    subscription = Subscription.objects.get(pk=subs_id)
    assert subscription.is_active() == True
    assert subscription.subscription_option.id == payment.subscription_option_id
    assert subscription.start_date.date() == payment.completed_or_failed_date.date()

@pytest.mark.django_db
def test_process_payment_success_webhook_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    request_url = url + 'webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404

@pytest.mark.django_db
def test_process_payment_failure_webhook():
    subscription_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.payment_failed'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'failed'
    request_url = url + 'webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment.status == -1

@pytest.mark.django_db
def test_process_payment_failure_webhook_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    webhook_payload['type'] = 'payment_intent.payment_failed'
    webhook_payload['data']['object']['id'] = stripe_pid
    webhook_payload['data']['object']['status'] = 'failed'
    request_url = url + 'webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404
