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

admin.site.register(Payment)