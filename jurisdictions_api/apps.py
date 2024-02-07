"""Defines the config class for the jurisdictions API."""

from django.apps import AppConfig


class JurisdictionsApiConfig(AppConfig):
    """Defines the configuration for the jurisdictions API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jurisdictions_api'
    verbose_name = 'Jurisdictions'
