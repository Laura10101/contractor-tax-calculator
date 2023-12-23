from django.db import models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Create your models here.

class SubscriptionOption(models.Model):
    subscription_months = models.IntegerField()
    subscription_price = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=6)
    is_active = models.BooleanField(null=False, blank=False)

    def vat(self):
        return round(float(self.subscription_price) * 0.20, 2)

    def total(self):
        return round(float(self.subscription_price) + self.vat(), 2)

    def __str__(self):
        return str(self.subscription_months) + ' month extension (£' + str(self.subscription_price) + ')'

class Subscription(models.Model):
    user_id = models.IntegerField()
    subscription_option = models.ForeignKey(
        SubscriptionOption,
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    start_date = models.DateTimeField(null=False, blank=False)

    def is_active(self):
        if self.subscription_option is None:
            return False
            
        subscription_months = self.subscription_option.subscription_months
        expiry_date = self.start_date + relativedelta(months=subscription_months)
        return date.today() <= datetime.strptime(expiry_date.strftime('%Y-%m-%d'), '%Y-%m-%d').date()

    def __str__(self):
        return 'Subscription for user ' + str(self.user_id)
