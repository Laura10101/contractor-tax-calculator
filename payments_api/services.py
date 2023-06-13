from .models import Payment 
from .stripe import *
from datetime import date 


def create_payment(subscription_id, requested_subscription_months, subtotal, currency):
    # Calculate VAT 
    vat = subtotal * 0.2
    # Calculate total
    total = subtotal + vat
    # Create new payment in the database 
    new_payment = Payment.objects.create(
        subscription_id=subscription_id,
        requested_subscription_months=requested_subscription_months,
        subtotal=subtotal,
        currency=currency,
        vat=vat,
        total=total
    )
    # Create the payment intention in Stripe and update the local payment record 
    # with the payment ID from Stripe and with the intent created status
    new_payment.stripe_pid, new_payment.client_secret = create_stripe_payment_intention(
        new_payment.total, new_payment.currency
        )
    new_payment.status = 2
    new_payment.save()

    # Return ID of newly created jurisdiction
    return new_payment.id, new_payment.client_secret

def confirm_payment(id, billing_street_1, billing_street_2, town_or_city, county, country, postcode, stripe_card_id):
    payment = Payment.objects.get(pkid)

    # Update the payment with the billing details in local record
    payment.billing_street_1=billing_street_1
    payment.billing_street_2=billing_street_2
    payment.town_or_city=town_or_city
    payment.county=county
    payment.country=country
    payment.postcode=postcode
    payment.stripe_card_id=stripe_card_id
    payment.save()

    # Confirm the payment with Stripe and update its status
    confirm_stripe_payment(payment.pid, payment.stripe_card_id)
    payment.status=3
    payment.intended_date=date.today()
    payment.save()

def complete_payment(stripe_pid):
    payment = Payment.objects.filter(stripe_pid__exact=id).update(
        status=4,
        created_or_failed_date=date.today()
        )

def fail_payment(stripe_pid, reason):
    payment = Payment.objects.filter(stripe_pid__exact=id).update(
        status=-1,
        created_or_failed_date=date.today(),
        stripe_error=reason
        )

def get_payment_status(id):
    payment = Payment.objects.get(pk=id)
    payment_statuses = {
        -1: 'failed',
        1: 'created',
        2: 'intended',
        3: 'pending',
        4: 'complete',
    }
    return payment_statuses[payment.status]