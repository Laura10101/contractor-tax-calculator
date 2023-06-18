from django.db import models
from datetime import date, timedelta

# Create your models here.

class Subscription(models.Model):
    user_id = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    subscription_months = models.IntegerField()

    def is_active(self):
        expiry_date = F(self.start_date) + relativedelta(months=self.subscription_months)
        return date.today() <= expiry_date

class SubscriptionOption(models.Model):
    subscription_months = models.IntegerField()
    subscription_price = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=6)
    is_active = models.BooleanField(null=False, blank=False)
