from django.contrib import admin
from .models import Payment

# Register your models here.
# Make payments admin readonly - this is for support only
# Code adapted from: https://thetldr.tech/how-to-create-django-admin-with-readonly-permission/
class BaseReadOnlyAdminMixin:
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class PaymentModelAdmin(BaseReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = (
        'subscription_id',
        'subscription_option_id',
        'stripe_pid',
        'status',
        'stripe_error',
        'total',
        'currency',
        'created_date',
        'intended_date',
        'completed_or_failed_date'
        )

admin.site.register(Payment, PaymentModelAdmin)