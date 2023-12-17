from datetime import date
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from stripe.error import InvalidRequestError
from .models import *
from .services import *
import pytest
from .stripe import *
from rest_framework.test import APIClient

from subscriptions_api.models import Subscription, SubscriptionOption

# Required fields on a payment
# subscription_id - The ID of the associated subscription
# stripe_pid - The Stripe ID for the payment
# status - 1 = 'created' when first created
#        - 2 = 'intended' when payment intention successfully created with stripe
#        - 3 = 'pending' when confirmation sent to Stripe
#        - 4 = 'complete' when payment completed and confirmed by Stripe
#        - -1 = 'failed' when payment failed in Stripe
# stripe_error - The details of the error from stripe
# subscription_option_id - The id of the subscription option being purchased
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
def get_mock_payment_id():
    subscription_id = 1
    subscription_option_id = 1
    total = 47.99
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    return id

# Test creating a payment
# Payment creation only requires the following fields:
# subscription_id, requested_subscription_months, subtotal, currency
@pytest.mark.django_db
def test_create_payment_with_null_data():
    subscription_id = None
    subscription_option_id = None
    total = None
    currency = None
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, subscription_option_id, total, currency)

@pytest.mark.django_db
def test_create_payment_with_null_subscription_id():
    subscription_id = None
    subscription_option_id = 1
    total = 47.99
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    assert id is not None
    payment = Payment.objects.get(pk=id)
    assert payment.subscription_id == subscription_id
    assert payment.subscription_option_id == subscription_option_id
    assert payment.total == total
    assert payment.currency == currency
    assert payment.status == 2
    assert payment.created_date.date() == date.today()
    assert payment.intended_date.date() == date.today()
    assert payment.stripe_pid is not None

@pytest.mark.django_db
def test_create_payment_with_null_subscription_option_id():
    subscription_id = 1
    subscription_option_id = None
    total = 47.99
    currency = 'GBP'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, subscription_option_id, total, currency)

@pytest.mark.django_db
def test_create_payment_with_null_subtotal():
    subscription_id = 1
    subscription_option_id = 1
    total = None
    currency = 'GBP'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, subscription_option_id, total, currency)

@pytest.mark.django_db
def test_create_payment_with_negative_subtotal():
    subscription_id = 1
    subscription_option_id = 1
    total = -47.99
    currency = 'GBP'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, subscription_option_id, total, currency)

@pytest.mark.django_db
def test_create_payment_with_invalid_currency_code():
    subscription_id = 1
    subscription_option_id = 1
    total = 47.99
    currency = 'Abracadabra'
    with pytest.raises(ValidationError):
        id = create_payment(subscription_id, subscription_option_id, total, currency)

@pytest.mark.django_db
def test_create_valid_payment():
    subscription_id = 1
    subscription_option_id = 1
    total = 47.99
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option_id, total, currency)
    assert id is not None
    payment = Payment.objects.get(pk=id)
    assert payment.subscription_id == subscription_id
    assert payment.subscription_option_id == subscription_option_id
    assert payment.total == total
    assert payment.currency == currency
    assert payment.status == 2
    assert payment.created_date.date() == date.today()
    assert payment.intended_date.date() == date.today()
    assert payment.stripe_pid is not None

# Test patching a payment with payment details
# Requires the following fields:
@pytest.mark.django_db
def test_update_payment_with_null_payment_id():
    #confirm_payment(id, stripe_card_id)
    id = None
    stripe_card_id = 'pm_card_gb'

    with pytest.raises(Payment.DoesNotExist):
        confirm_payment(id, stripe_card_id)

@pytest.mark.django_db
def test_update_payment_with_non_existent_payment_id():
    #confirm_payment(id, stripe_card_id)
    id = 57912
    stripe_card_id = 'pm_card_gb'

    with pytest.raises(Payment.DoesNotExist):
        confirm_payment(id, stripe_card_id)

@pytest.mark.django_db
def test_update_payment_with_null_card_id():
    #confirm_payment(id, stripe_card_id)
    id = get_mock_payment_id()
    stripe_card_id = None

    with pytest.raises(InvalidRequestError):
        confirm_payment(id, stripe_card_id)

@pytest.mark.django_db
def test_update_payment():
    id = get_mock_payment_id()
    stripe_card_id = 'pm_card_gb'
    
    confirm_payment(id, stripe_card_id)

    payment = Payment.objects.get(pk=id)
    assert payment.status == 3
    assert payment.stripe_error is None
    assert payment.stripe_pid is not None

# Test posting the payment result
@pytest.mark.django_db
def test_process_payment_success():
    client = APIClient()
    subs_url = '/api/subscriptions/'

    subscription_option = SubscriptionOption.objects.create(
        subscription_months=6,
        subscription_price=4.99,
        is_active=True
    )
    
    subscription_id = Subscription.objects.create(
        subscription_option = subscription_option,
        user_id = 479,
        start_date = datetime.now()
    )

    total = subscription_option.total()
    currency = 'GBP'
    id, _ = create_payment(subscription_id, subscription_option.id, total, currency)

    payment = Payment.objects.get(pk=id)
    print(payment.stripe_pid)

    complete_payment(payment.stripe_pid)

    payment = Payment.objects.get(pk=id)
    assert payment.status == 4

    subs_id = payment.subscription_id

    response = client.get(subs_url + str(subs_id) + '/')
    print(response.data)
    assert response.data['is_active'] == True
    assert response.data['subscription_option_id'] == payment.requested_subscription_months
    assert response.data['start_date'] == payment.completed_or_failed_date

@pytest.mark.django_db
def test_process_payment_success_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    with pytest.raises(Payment.DoesNotExist):
        complete_payment(stripe_pid)

@pytest.mark.django_db
def test_process_payment_failure():
    reason = 'Some stripe reason'

    subscription_id = 1
    requested_subscription_months = 6
    subtotal = 42.30
    currency = 'GBP'
    id, _ = create_payment(subscription_id, requested_subscription_months, subtotal, currency)

    payment = Payment.objects.get(pk=id)

    id = fail_payment(payment.stripe_pid, reason)

    payment = Payment.objects.get(pk=id)
    assert payment.status == -1
    assert payment.stripe_error == reason

@pytest.mark.django_db
def test_process_payment_failure_with_unknown_stripe_pid():
    stripe_pid = 'pid_imadethisup'
    reason = 'Some stripe reason'
    with pytest.raises(Payment.DoesNotExist):
        fail_payment(stripe_pid, reason)