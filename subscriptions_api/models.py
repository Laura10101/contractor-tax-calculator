from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta

# Create your models here.

class Subscription(models.Model):
    user_id = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    subscription_months = models.IntegerField()

    def is_active(self):
        expiry_date = self.start_date + relativedelta(months=self.subscription_months)
        return date.today() <= expiry_date
