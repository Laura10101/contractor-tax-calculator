from django.contrib import admin
from .models import Payment

from .forms import PaymentForm

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm

admin.site.register(Payment, PaymentAdmin)