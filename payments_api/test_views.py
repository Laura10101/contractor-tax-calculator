from datetime import date
from dateutil.relativedelta import relativedelta
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from .models import *
from .services import *
from .views import *
import pytest
import time
import stripe
from contractor_tax_calculator import settings

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
        subscription_option=subscription_option,
        user_id=479,
        start_date=datetime.now() - relativedelta(months=2)
    )

# Test creating a payment
# Format for POST payload on payments API
# {
#   'user_id': x,
#   'subscription_option_id': x,
#   'total': x.y,
#   'currency': 'ZZZ'
# }


@pytest.mark.django_db
def test_post_payment_with_null_data():
    user_id = None
    subscription_option_id = None
    total = None
    currency = None

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_payment_with_null_user_id():
    user_id = None
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_payment_with_null_subscription_option_id():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = None
    total = 42.30
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_payment_with_negative_subscription_option_id():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = -6
    total = 42.30
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_payment_with_null_total():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = None
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_payment_with_negative_total():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = -42.30
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_payment_with_invalid_currency_code():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'G'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_post_valid_payment():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'

    data = {
        'user_id': user_id,
        'subscription_option_id': subscription_option_id,
        'total': total,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 200
    id = response.data['payment_id']

    assert id is not None
    payment = Payment.objects.get(pk=id)
    assert payment.user_id == user_id
    assert payment.subscription_option_id == subscription_option_id
    assert payment.total == total
    assert payment.currency == currency
    assert payment.status == 2
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
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    data = {
        'stripe_card_id': None
    }
    response = client.patch(url + str(None) + '/', data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_payment_with_null_payment_id():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    data = {
        'stripe_card_id': 'pm_card_gb'
    }
    response = client.patch(url + str(None) + '/', data, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_patch_payment_with_null_stripe_card_id():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    data = {
        'stripe_card_id': None
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_payment_with_non_string_stripe_card_id():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    data = {
        'stripe_card_id': 1234
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_patch_valid_payment():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    data = {
        'stripe_card_id': 'pm_card_gb'
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 200
    assert response.data is not None

    assert response.data['result'] in ['processing', 'succeeded']

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
            "client_secret":
            "pi_1JKS5I2x6R10KRrhk9GzY4BM_secret_N1kiKaTvicujcDGMskLXGasty",
            "confirmation_method": "automatic",
            "created": 1628014284,
            "currency": "usd",
            "customer": None,
            "description": "",
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

# This function generates the signature header required when testing webhooks
# The code is lifted from the Stripe Python library's webhook tests
# https://github.com/stripe/stripe-python/blob/master/tests/test_webhook.py


def generate_stripe_webhook_signature(**kwargs):
    timestamp = kwargs.get("timestamp", int(time.time()))
    payload = kwargs.get("payload", webhook_payload)
    secret = kwargs.get("secret", settings.STRIPE_WH_SECRET)
    scheme = kwargs.get("scheme", stripe.WebhookSignature.EXPECTED_SCHEME)
    signature = kwargs.get("signature", None)
    if signature is None:
        payload_to_sign = "%d.%s" % (timestamp, payload)
        signature = stripe.WebhookSignature._compute_signature(
            payload_to_sign, secret
        )
    header = "t=%d,%s=%s" % (timestamp, scheme, signature)
    return header


@pytest.mark.django_db
def test_process_payment_success_webhook():
    subscription = create_mock_subscription(create_mock_subscription_option())
    subscription_id = subscription.id
    user_id = subscription.user_id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    encoded_payload = json.dumps(webhook_payload).replace(' ', '')
    request_url = url + 'webhooks/'
    signature = generate_stripe_webhook_signature(payload=encoded_payload)
    client.credentials(
        HTTP_STRIPE_SIGNATURE=signature
    )
    response = client.post(request_url, data=webhook_payload, format="json")
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment.status == 4

    subscription = Subscription.objects.get(pk=subscription_id)
    assert subscription.is_active() is True
    assert subscription_option_id == payment.subscription_option_id
    pcofd = payment.completed_or_failed_date.date()
    assert subscription.start_date.date() == pcofd


@pytest.mark.django_db
def test_process_payment_success_webhook_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    encoded_payload = json.dumps(webhook_payload).replace(' ', '')
    request_url = url + 'webhooks/'
    signature = generate_stripe_webhook_signature(payload=encoded_payload)
    client.credentials(
        HTTP_STRIPE_SIGNATURE=signature
    )
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404


@pytest.mark.django_db
def test_process_payment_failure_webhook():
    user_id = create_mock_subscription(create_mock_subscription_option()).id
    subscription_option_id = create_mock_subscription_option().id
    total = 42.30
    currency = 'GBP'
    id, _ = create_payment(user_id, subscription_option_id, total, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.payment_failed'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'failed'
    encoded_payload = json.dumps(webhook_payload).replace(' ', '')
    request_url = url + 'webhooks/'
    signature = generate_stripe_webhook_signature(payload=encoded_payload)
    client.credentials(
        HTTP_STRIPE_SIGNATURE=signature
    )
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
    encoded_payload = json.dumps(webhook_payload).replace(' ', '')
    request_url = url + 'webhooks/'
    signature = generate_stripe_webhook_signature(payload=encoded_payload)
    client.credentials(
        HTTP_STRIPE_SIGNATURE=signature
    )
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404
