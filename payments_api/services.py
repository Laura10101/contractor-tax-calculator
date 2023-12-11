from .models import Payment 
from .stripe import *
from decimal import *
from datetime import datetime, date
from django.core.exceptions import ValidationError


def create_payment(subscription_id, subscription_option_id, total, currency):
    if not isinstance(total, float):
        raise ValidationError('Parameter total must be a valid float to 2 decimal places')

    # Create new payment in the database 
    new_payment = Payment()
    new_payment.subscription_id=subscription_id
    new_payment.subscription_option_id=subscription_option_id
    new_payment.currency=currency
    new_payment.total=round(total, 2)
    new_payment.full_clean()
    new_payment.save()

    # Create the payment intention in Stripe and update the local payment record 
    # with the payment ID from Stripe and with the intent created status
    new_payment.stripe_pid, new_payment.client_secret = create_stripe_payment_intention(
        new_payment.total, new_payment.currency
        )
    new_payment.intended_date=datetime.now()
    new_payment.status = 2
    new_payment.save()

    # Return ID of newly created jurisdiction
    return new_payment.id, new_payment.client_secret

def confirm_payment(id, stripe_card_id):
    payment = Payment.objects.get(pk=id)

    # Confirm the payment with Stripe and update its status
    success, status_or_error = confirm_stripe_payment(payment.stripe_pid, stripe_card_id)

    if success and status_or_error in ['processing', 'succeeded']:
        print('Payment confirmation succeeded')
        payment.status=3
        payment.intended_date=datetime.now()
        payment.save()
        return True, 'succeeded'
    else:
        print('Payment failed with reason ' + status_or_error)
        payment.status=-1
        payment.stripe_error = status_or_error
        payment.completed_or_failed_date=datetime.now()
        payment.save()
        return False, 'failed with reason:''' + status_or_error + '.'''

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
    return payment_statuses[payment.status], payment.stripe_error