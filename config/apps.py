"""Defines the config class for the config app."""
from django.apps import AppConfig


class ConfigConfig(AppConfig):
    """Configuration for the config app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'
