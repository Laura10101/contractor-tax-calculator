"""Define helper methods for Stripe integration."""

from django.conf import settings

import stripe

# Retrieve keys from env.py
stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY


def create_stripe_payment_intention(amount, currency):
    """Create payment intention for Stripe."""
    """Amount is in GBP."""

    # Then create payment intent
    # This code is from the CI video by Tim Nelson
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        # From Stripe documentation:
        # 'Amount intended to be collected by this PaymentIntent.
        # A positive integer representing how much to charge in
        # the smallest currency unit'
        # https://stripe.com/docs/api/payment_intents/create
        amount=int(amount * 100),
        currency=currency,
    )
    return intent.id, intent.client_secret


def confirm_stripe_payment(stripe_pid, stripe_card_id):
    """Confirm the payment intent for Stripe."""
    # This code is adapted from the Stripe documentation
    # https://stripe.com/docs/api/payment_intents/confirm?lang=python
    stripe.api_key = stripe_secret_key
    try:
        payment_intent = stripe.PaymentIntent.confirm(
            stripe_pid,
            payment_method=stripe_card_id,
            capture_method='automatic_async'
        )
        return payment_intent.status
    except stripe.error.CardError as ex:
        return str(ex)
