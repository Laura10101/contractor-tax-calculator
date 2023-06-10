from .models import Payment 
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
    new_payment.status = 2
    new_payment.save()

    # Return ID of newly created jurisdiction
    return new_payment.id

def confirm_payment(id, billing_street_1, billing_street_2, town_or_city, county, country, postcode, 
    card_number, expiry_date, ccv2):
    payment = Payment.objects.filter(pk__exact=id).update(
        billing_street_1=billing_street_1,
        billing_street_2=billing_street_2, 
        town_or_city=town_or_city, 
        county=county, 
        country=country, 
        postcode=postcode, 
        card_number=card_number, 
        expiry_date=expiry_date, 
        ccv2=ccv2,
        status=3,
        intended_date=date.today()
        )

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