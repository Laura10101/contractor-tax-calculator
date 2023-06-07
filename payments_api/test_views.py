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
url = '/api/payments/'

# Test creating a subscription
@pytest.mark.django_db
from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

# Test creating a payment
# Format for POST payload on payments API
# {
#   'subscription_id': x,
#   'requested_months': x,
#   'subtotal': x.y,
#   'currency': 'ZZZ'
# }
@pytest.mark.django_db
def test_create_payment_with_null_data():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_null_subscription_id():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_null_months():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_negative_months():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_null_subtotal():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_negative_subtotal():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_invalid_currency_code():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_valid_payment():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)
    assert id is not None
    payment = Payments.objects.get(pk=id)
    assert payment.subscription_id == subscription_id
    assert payment.requested_subscription_months == requested_subscription_months
    assert payment.subtotal == subtotal
    assert payment.vat == (subtotal * 0.19)
    assert payment.total == payment.subtotal + payment.vat
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
def test_patch_payment_with_null_payment_data():
    pass

def test_patch_payment_with_null_street1():
    pass

def test_patch_payment_with_null_street2():
    pass

def test_patch_payment_with_null_city():
    pass

def test_patch_payment_with_null_county():
    pass

def test_patch_payment_with_null_country():
    pass

def test_patch_payment_with_null_postcode():
    pass

def test_patch_payment_with_null_card_number():
    pass

def test_patch_payment_with_null_expiry():
    pass

def test_patch_payment_with_null_ccv2():
    pass

def test_patch_payment():
    pass

# Test posting the payment result
# Expected payload for Stripe webhook will be a payment intent object
# wrapped in an event object
# Event objects: https://stripe.com/docs/api/events/object
# Payment intent objects: https://stripe.com/docs/api/payment_intents

webhook_payload = {
    "id": "evt_1NGObyFkVBiDxSnkSOAnG6mj",
    "object": "event",
    "api_version": null,
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
            "application": null,
            "application_fee_amount": null,
            "automatic_payment_methods": null,
            "canceled_at": null,
            "cancellation_reason": null,
            "capture_method": "automatic",
            "client_secret": "pi_1JKS5I2x6R10KRrhk9GzY4BM_secret_N1kiKaTvicujcDGMskLXGasty",
            "confirmation_method": "automatic",
            "created": 1628014284,
            "currency": "usd",
            "customer": null,
            "description": "Created by stripe.com/docs demo",
            "invoice": null,
            "last_payment_error": null,
            "latest_charge": null,
            "livemode": false,
            "metadata": {},
            "next_action": null,
            "on_behalf_of": null,
            "payment_method": null,
            "payment_method_options": {
                "card": {
                    "installments": null,
                    "mandate_options": null,
                    "network": null,
                    "request_three_d_secure": "automatic"
                }
            },
            "payment_method_types": [
                "card"
            ],
            "processing": null,
            "receipt_email": null,
            "review": null,
            "setup_future_usage": null,
            "shipping": null,
            "statement_descriptor": null,
            "statement_descriptor_suffix": null,
            "status": "requires_payment_method",
            "transfer_data": null,
            "transfer_group": null
        }
    },
    "livemode": false,
    "pending_webhooks": 0,
    "request": {
        "id": null,
        "idempotency_key": null
    },
    "type": ""
}

def test_stripe_webhook_payment_success():
    webhook_payload['type'] == 'payment_intent.succeeded'
    webhook_payload['data']['object']['status'] == 'succeeded'
    request_url = url + '/stripe-webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200

def test_stripe_webhook_payment_failure():
    webhook_payload['type'] == 'payment_intent.payment_failed'
    webhook_payload['data']['object']['status'] == 'failed'
    request_url = url + '/stripe_webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200