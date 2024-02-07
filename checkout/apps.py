"""Defines the config class for the checkout app."""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """Configure the checkout app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'
