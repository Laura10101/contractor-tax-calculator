"""Defines the config class for the forms API."""
from django.apps import AppConfig


class FormsApiConfig(AppConfig):
    """Defines the configuration for the forms API."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forms_api'
    verbose_name = 'Forms'

    def ready(self):
        import forms_api.signals
