"""Defines the config class for the subscriptions API."""
from django.apps import AppConfig


class SubscriptionsApiConfig(AppConfig):
    """Defines the configuration for the subscriptions API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions_api'
    verbose_name = 'Subscriptions'

    def ready(self):
        """Set up signals when app is ready."""
        
        import subscriptions_api.signals
