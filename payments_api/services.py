"""Define service methods for the payments API."""

from .models import Payment
from .stripe import (
    create_stripe_payment_intention,
    confirm_stripe_payment
)
from decimal import *
from datetime import datetime, date
from django.core.exceptions import ValidationError


def create_payment(user_id, subscription_option_id, total, currency):
    """Create a new payment and raise payment intent with Stripe."""
    if not isinstance(total, float) and not isinstance(total, int):
        raise ValidationError(
            'Parameter total must be a valid integer or a ' +
            'float to 2 decimal places'
        )

    # Create new payment in the database
    new_payment = Payment()
    new_payment.user_id = user_id
    new_payment.subscription_option_id = subscription_option_id
    new_payment.currency = currency
    new_payment.total = round(total, 2)
    new_payment.full_clean()
    new_payment.save()

    # Create the payment intention in Stripe and update the
    # local payment record with the payment ID from Stripe
    # and with the intent created status
    pid, cs = create_stripe_payment_intention(
        new_payment.total, new_payment.currency
    )
    new_payment.stripe_pid = pid
    new_payment.client_secret = cs
    new_payment.intended_date = datetime.now()
    new_payment.status = 2
    new_payment.save()

    # Return ID of newly created jurisdiction
    return new_payment.id, new_payment.client_secret


def confirm_payment(id, stripe_card_id):
    """Confirm a payment with Stripe and updated payment status."""
    payment = Payment.objects.get(pk=id)

    # Confirm the payment with Stripe and update its status
    status_or_error = confirm_stripe_payment(
        payment.stripe_pid, stripe_card_id
    )

    if status_or_error in ['processing', 'succeeded']:
        payment.status = 3
        payment.intended_date = datetime.now()
        payment.save()
        return status_or_error
    else:
        payment.status = -1
        payment.stripe_error = status_or_error
        payment.completed_or_failed_date = datetime.now()
        payment.save()
        return 'failed with reason:''' + status_or_error + '.'''


def complete_payment(stripe_pid):
    """Update the status of a payment to complete."""

    payments = Payment.objects.filter(stripe_pid__exact=stripe_pid)

    if payments.count() == 0:
        raise Payment.DoesNotExist()

    if payments.count() > 1:
        raise ValidationError(
            'Multiple payments found for Stripe PID = ' + stripe_pid
        )

    payment = payments.first()

    if payment.status == 4:
        raise ValidationError(
            'Payment with stripe_pid = ' + stripe_pid +
            ' is already completed. Cannot complete again.'
        )

    payment.status = 4
    payment.completed_or_failed_date = date.today()
    payment.full_clean()
    payment.save()


def fail_payment(stripe_pid, reason):
    """Update the status of a payment to failed and save reason."""

    payments = Payment.objects.filter(stripe_pid__exact=stripe_pid)

    if payments.count() == 0:
        raise Payment.DoesNotExist()

    payments.update(
        status=-1,
        completed_or_failed_date=date.today(),
        stripe_error=reason
        )


def get_payment_status(id):
    """Get the current status of a payment based on ID."""
    payment = Payment.objects.get(pk=id)
    payment_statuses = {
        -1: 'failed',
        1: 'created',
        2: 'intended',
        3: 'pending',
        4: 'complete',
    }
    return payment_statuses[payment.status], payment.stripe_error


def get_recent_payments(user_id):
    """Get a list of the recent payments for a given user ID."""
    payments = Payment.objects.filter(
        user_id__exact=user_id
    ).order_by('-created_date', '-status')
    if payments.count() <= 5:
        return payments.all()
    else:
        return payments.all()[0:5]
