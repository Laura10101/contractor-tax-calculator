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

# Test creating a payment
# Format for POST payload on payments API
# {
#   'subscription_id': x,
#   'requested_months': x,
#   'subtotal': x.y,
#   'currency': 'ZZZ'
# }
@pytest.mark.django_db
def test_post_payment_with_null_data():
    susbcription_id = None
    requested_subscription_months = None
    subtotal = None
    currency = None

    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_null_subscription_id():
    susbcription_id = None
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'

    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_null_months():
    susbcription_id = 1
    requested_subscription_months = None
    subtotal = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_negative_months():
    susbcription_id = 1
    requested_subscription_months = -6
    subtotal = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_null_subtotal():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = None
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_negative_subtotal():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = -42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_payment_with_invalid_currency_code():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'G'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400

def test_post_valid_payment():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    
    data = {
        'subscription_id': subscription_id,
        'requested_months': requested_subscription_months,
        'subtotal': subtotal,
        'currency': currency
    }
    response = client.post(url, data, format='json')
    assert response.status_code == 400
    id = response.data['id']

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
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = None
    billing_street_2 = None
    town_or_city = None
    county = None
    country = None
    postcode = None
    card_number = None
    expiry_date = None
    ccv2 = None
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_street1():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)
    
    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439

    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_street2():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = None
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_city():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = None
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_county():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = None
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_country():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = None
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_postcode():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = None
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_card_number():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = None
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_expiry():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = None
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_null_ccv2():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = None
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111'
    expiry_date = date.today()
    ccv2 = 439
    
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment is not None
    assert payment.billing_street_1 == billing_street_1
    assert payment.billing_street_2 == billing_street_2
    assert payment.town_or_city == town_or_city
    assert payment.county == county
    assert payment.country == country
    assert payment.postcode == postcode
    assert payment.card_number == card_number
    assert payment.expiry_date == expiry_date
    assert payment.ccv2 == ccv2
    assert payment.status == 3
    assert payment.stripe_pid is not None

def test_patch_payment_with_short_card_number():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 111'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_long_card_number():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111 1'
    expiry_date = date.today()
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_non_date_expiry():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111 1'
    expiry_date = 51085
    ccv2 = 439
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_non_numeric_ccv2():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111 1'
    expiry_date = date.today()
    ccv2 = '439'
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

def test_patch_payment_with_nonexistent_payment_id():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    billing_street_1 = '4 Maine Street'
    billing_street_2 = 'St Leonards'
    town_or_city = 'Exeter'
    county = 'Devon'
    country = 'United Kingdom'
    postcode = 'EX2 7ST'
    card_number = '1111 1111 1111 1111 1'
    expiry_date = date.today()
    ccv2 = '439'
    
    data = {
        'billing_address' {
            'billing_street_1': billing_street_1,
            'billing_street_2': billing_street_2,
            'town_or_city': town_or_city,
            'county': county,
            'country': country,
            'postcode': postcode
        }
        'payment_details' {
            'card_number': card_number,
            'expiry_date': expiry_date,
            'ccv2': ccv2
        }
    }
    response = client.patch(url + str(id) + '/', data, format='json')
    assert response.status_code == 400

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

def test_process_payment_success_webhook():
    client = APIClient()
    subs_url = '/api/subscriptions/'

    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    request_url = url + 'stripe-webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment.status == 4

    subs_id = payment.subscription_id

    response = client.get(subs_url + str(subs_id) + '/')
    assert response.data['is_active'] == True
    assert response.data['subscription_months'] == payment.requested_subscription_months
    assert response.data['start_date'] == payment.completed_or_failed_date

def test_process_payment_success_webhook_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'

    webhook_payload['type'] = 'payment_intent.succeeded'
    webhook_payload['data']['object']['id'] = stripe_pid
    webhook_payload['data']['object']['status'] = 'succeeded'
    request_url = url + 'stripe-webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404

def test_process_payment_failure_webhook():
    reason = 'Some stripe reason'

    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    payment = Payment.objects.get(pk=id)

    webhook_payload['type'] = 'payment_intent.payment_failed'
    webhook_payload['data']['object']['id'] = payment.stripe_pid
    webhook_payload['data']['object']['status'] = 'failed'
    request_url = url + 'stripe_webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 200

    payment = Payment.objects.get(pk=id)
    assert payment.status == -1
    assert payment.stripe_error == reason

def test_process_payment_failure_webhook_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    webhook_payload['type'] = 'payment_intent.payment_failed'
    webhook_payload['data']['object']['id'] = stripe_pid
    webhook_payload['data']['object']['status'] = 'failed'
    request_url = url + 'stripe_webhooks/'
    response = client.post(request_url, webhook_payload, format='json')
    assert response.status_code == 404
