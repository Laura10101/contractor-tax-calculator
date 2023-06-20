from django.contrib import admin
from .models import Subscription, SubscriptionOption
from .forms import SubscriptionForm

class SubscriptionAdmin(admin.ModelAdmin):
    form = SubscriptionForm

# Register your models here.
admin.site.register(SubscriptionOption)
admin.site.register(Subscription, SubscriptionAdmin)
