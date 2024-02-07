"""Add the Payment model to the admin app."""

from django.contrib import admin
from .models import Payment

from .forms import PaymentForm


class PaymentAdmin(admin.ModelAdmin):
    """Admin configuration for the Payment model."""
    form = PaymentForm


admin.site.register(Payment, PaymentAdmin)
