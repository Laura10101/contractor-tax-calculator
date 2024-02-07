"""Add the Subscription form and SubscriptionOption model to the admin app."""

from django.contrib import admin
from .models import Subscription, SubscriptionOption
from .forms import SubscriptionForm


class SubscriptionAdmin(admin.ModelAdmin):
    """Configure admin form for Subscription form."""

    form = SubscriptionForm


# Register your models here.
admin.site.register(SubscriptionOption)
admin.site.register(Subscription, SubscriptionAdmin)
