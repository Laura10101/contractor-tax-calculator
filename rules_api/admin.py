"""Add the RuleSet form to the admin app."""

from django.contrib import admin
from .models import TaxCategory


# Register your models here.
admin.site.register(TaxCategory)
