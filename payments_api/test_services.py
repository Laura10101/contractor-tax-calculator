from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import *
from .services import *
import pytest

# Required fields on a payment
# subscription_id - The ID of the associated subscription
# stripe_pid - The Stripe ID for the payment
# status - 1 = 'created' when first created
#        - 2 = 'intended' when payment intention successfully created with stripe
#        - 3 = 'pending' when confirmation sent to Stripe
#        - 4 = 'complete' when payment completed and confirmed by Stripe
#        - -1 = 'failed' when payment failed in Stripe
# stripe_error - The details of the error from stripe
# requested_subscription_months - The number of months by which to extend the subscription
#   if payment is successful
# subtotal - The subtotal for the payment
# vat - The amount of VAT payable
# total - subtotal + vat
# currency - Currency of the payment (three digit code)
# billing_street_1 - The first street line of the billing address
# billing_street_2 - The second line of the billing address. Allow null.
# town_or_city - The billing address town or city
# county - The billing address county. Allow null.
# country - The billing address country
# postcode - The billing address postcode. Allow null.
# card_number - The payment card number
# expiry_date - The expiry date on the card
# ccv2 - The CCV2 code for the card
# created_date - The date on which the payment was created
# intended_date - The date on which the payment intention was confirmed in stripe
# completed_or_failed_date - The date on which the payment completed in Stripe

# Test creating a payment
# Payment creation only requires the following fields:
# subscription_id, requested_subscription_months, subtotal, currency
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
def test_confirm_payment_success():
    pass

def test_fail_payment():
    pass