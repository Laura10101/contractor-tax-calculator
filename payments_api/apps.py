"""Defines the config class for the payments API."""
from django.apps import AppConfig


class PaymentsApiConfig(AppConfig):
    """Defines the configuration for the payments API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments_api'
    verbose_name = 'Payments'
