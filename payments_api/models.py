from django.db import models

# Create your models here.

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


class Payment(models.Model):
    # Add class attributes 
    subscription_id = IntegerField(null=False, blank=False)
    stripe_pid = CharField(max_length=50, null=False, blank=False)
    status = IntegerField(null=False, blank=False, Default=1)
    stripe_error = CharField(max_length=50, null=False, blank=False)
    requested_subscription_months = IntegerField(null=False, blank=False)
    subtotal = DecimalField(decimal_places=2, null=False, blank=False)
    vat = DecimalField(decimal_places=2, null=False, blank=False)
    total = DecimalField(decimal_places=2, null=False, blank=False)
    currency = CharField(max_length=3, null=False, blank=False)
    billing_street_1 = CharField(max_length=50, null=True, blank=True)
    billing_street_2 = CharField(max_length=50, null=True, blank=True)
    town_or_city = CharField(max_length=50, null=True, blank=True)
    county = CharField(max_length=50, null=True, blank=True)
    country = CharField(max_length=50, null=True, blank=True)
    postcode = CharField(max_length = 10, null=True, blank=True)
    card_number = CharField(max_length=19, null=True, blank=True)
    expiry_date = DateTimeField(null=False, blank=False)
    ccv2 = IntegerField(null=False, blank=False)
    created_date = DateTimeField(auto_now_add=True, null=False, blank=False)
    intended_date = DateTimeField(null=False, blank=False)
    completed_or_failed_date = DateTimeField(null=False, blank=False)

