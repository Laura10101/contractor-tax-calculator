"""Add the Jurisdiction model to the admin app."""

from django.contrib import admin
from .models import Jurisdiction

# Register your models here.
admin.site.register(Jurisdiction)
