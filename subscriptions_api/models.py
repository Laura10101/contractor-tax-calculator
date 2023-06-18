from django.db import models
from datetime import date, timedelta

# Create your models here.

class SubscriptionOption(models.Model):
    subscription_months = models.IntegerField()
    subscription_price = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=6)
    is_active = models.BooleanField(null=False, blank=False)

    def vat(self):
        return self.subscription_price * 0.20

    def total(self):
        return self.subscription_price + self.vat()

class Subscription(models.Model):
    user_id = models.IntegerField()
    subscription_option = models.ForeignKey(
        SubscriptionOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    start_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def is_active(self):
        subscription_months = self.subscription_option.subscription_months
        expiry_date = F(self.start_date) + relativedelta(months=subscription_months)
        return date.today() <= expiry_date
