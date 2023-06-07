from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_null_months():
    susbcription_id = 1
    requested_subscription_months = None
    subtotal = 42.30
    currency = 'GBP'
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_negative_months():
    susbcription_id = 1
    requested_subscription_months = -6
    subtotal = 42.30
    currency = 'GBP'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_null_subtotal():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = None
    currency = 'GBP'
    with pytest.raises(IntegrityError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_negative_subtotal():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = -42.30
    currency = 'GBP'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_payment_with_invalid_currency_code():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'G'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

def test_create_valid_payment():
    susbcription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
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
# Requires the following fields:
# billing_street_1, billing_street_2, town_or_city, county, country, postcode, card_number, expiry_date, ccv2
def test_update_payment_with_null_payment_data():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_street1():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_street2():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_city():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_county():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_country():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_postcode():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_card_number():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_expiry():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_null_ccv2():
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
    with pytest.raises(IntegrityError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment():
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
    
    confirm_payment(
        id,
        billing_street_1, billing_street_2, town_or_city, county, country, postcode,
        card_number, expiry_date, ccv2
    )

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

def test_update_payment_with_short_card_number():
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
    with pytest.raises(ValidationError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_long_card_number():
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
    with pytest.raises(ValidationError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_non_date_expiry():
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
    with pytest.raises(ValidationError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_non_numeric_ccv2():
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
    with pytest.raises(ValidationError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

def test_update_payment_with_nonexistent_payment_id():
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
    with pytest.raises(ValidationError):
        confirm_payment(
            id,
            billing_street_1, billing_street_2, town_or_city, county, country, postcode,
            card_number, expiry_date, ccv2
        )

# Test posting the payment result
def test_process_payment_success():
    client = APIClient()
    subs_url = '/api/subscriptions/'

    stripe_pid = 'TBC'
    id = complete_payment(stripe_pid)

    payment = Payment.objects.get(pk=id)
    assert payment.status == 4

    subs_id = payment.subscription_id

    response = client.get(subs_url + str(subs_id) + '/')
    assert response.data['is_active'] == True
    assert response.data['subscription_months'] == payment.requested_subscription_months
    assert response.data['start_date'] == payment.completed_or_failed_date

def test_process_payment_success_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    with pytest.raises(ObjectDoesNotExist):
        complete_payment(stripe_pid)

def test_process_payment_failure():
    stripe_pid = 'TBC'
    reason = 'Some stripe reason'
    id = fail_payment(stripe_pid, reason)

    payment = Payment.objects.get(pk=id)
    assert payment.status == -1

def test_process_payment_failure_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    reason = 'Some stripe reason'
    with pytest.raises(ObjectDoesNotExist):
        fail_payment(stripe_pid, reason)