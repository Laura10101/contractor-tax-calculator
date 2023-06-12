from django.conf import settings

import stripe

# Retrieve keys from env.py
stripe_public_key = settings.STRIPE_PUBLIC_KEY
stripe_secret_key = settings.STRIPE_SECRET_KEY

# Create payment intention for Stripe 
def create_stripe_payment_intention(amount, currency):
    # Then create payment intent
    # This code is from the CI video by Tim Nelson 
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )
    return intent.id

# Confirm the payment intent for Stripe 
def confirm_stripe_payment(stripe_pid, stripe_card_id):
    # This code is adapted from the Stripe documentation 
    # https://stripe.com/docs/api/payment_intents/confirm?lang=python
    result = stripe.PaymentIntent.confirm(
        stripe_pid,
        payment_method=stripe_card_id,
        capture_method='automatic_async'
    )

    