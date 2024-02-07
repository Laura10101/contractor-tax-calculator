"""Defines the config class for the calculations app."""
from django.apps import AppConfig


class CalculationsConfig(AppConfig):
    """Configuration for the calculations app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calculations'
