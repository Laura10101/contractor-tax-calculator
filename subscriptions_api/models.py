"""Define models for the Subscription API."""

from django.db import models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class SubscriptionOption(models.Model):
    """Define a subscription option."""
    """Represents an offer of a price for a fixed number"""
    """of months."""

    subscription_months = models.IntegerField()
    subscription_price = models.DecimalField(
        decimal_places=2,
        null=False,
        blank=False,
        max_digits=6
    )
    is_active = models.BooleanField(null=False, blank=False)

    def vat(self):
        """Calculate VAT on the subscription option."""

        return round(float(self.subscription_price) * 0.20, 2)

    def total(self):
        """Calculate the total for the subscription option."""
        """Includes VAT."""

        return round(float(self.subscription_price) + self.vat(), 2)

    def __str__(self):
        """Represent the subscription option as a string."""

        string = str(self.subscription_months) + ' month extension (£'
        string = string + str(self.subscription_price) + ')'
        return string


class Subscription(models.Model):
    """Define subscription model."""
    """Represent a user's current subscription."""

    user_id = models.IntegerField()
    subscription_option = models.ForeignKey(
        SubscriptionOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    start_date = models.DateTimeField(null=False, blank=False)

    def is_active(self):
        """Check if the subscription is active."""

        if self.subscription_option is None:
            return False

        subscription_months = self.subscription_option.subscription_months

        expiry_date = self.start_date + relativedelta(
            months=subscription_months
        )

        return date.today() <= datetime.strptime(
            expiry_date.strftime('%Y-%m-%d'),
            '%Y-%m-%d'
        ).date()

    def __str__(self):
        """Represent the subscription as a string."""

        return 'Subscription for user ' + str(self.user_id)
