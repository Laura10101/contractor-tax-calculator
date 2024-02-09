"""Define payment model."""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from subscriptions_api.models import SubscriptionOption

# Create your models here.

# Required fields on a payment
# subscription_id - The ID of the associated subscription
# stripe_pid - The Stripe ID for the payment
# status - 1 = 'created' when first created
#        - 2 = 'intended' when payment intention successfully created
#        - 3 = 'pending' when confirmation sent to Stripe
#        - 4 = 'complete' when payment completed and confirmed by Stripe
#        - -1 = 'failed' when payment failed in Stripe
# stripe_error - The details of the error from stripe
# requested_subscription_months - The number of months by which to extend
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
# intended_date - The date on which the payment intention was confirmed
# completed_or_failed_date - The date on which the payment completed in Stripe


class Payment(models.Model):
    """Payment model."""

    # Add class attributes
    user_id = models.IntegerField(null=False, blank=False)
    subscription_option_id = models.IntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )

    stripe_pid = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.IntegerField(
        null=False,
        blank=False,
        default=1,
        validators=[MinValueValidator(0.0)]
    )

    stripe_error = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    total = models.FloatField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0.0)]
    )

    currency = models.CharField(max_length=3, null=False, blank=False)

    created_date = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    intended_date = models.DateTimeField(null=True, blank=True)
    completed_or_failed_date = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        """Represent this payment as a string."""

        subscription_length = str(
            SubscriptionOption.objects.get(
                pk=self.subscription_option_id
            ).subscription_months
        )
        string = 'Payment #' + str(self.id) + ' of ' + str(self.total)
        string = string + ' for ' + subscription_length
        string = string + ' month extension to subscription '
        string = string + ' for user ' + str(self.user_id)
        return string
