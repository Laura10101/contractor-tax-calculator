"""Defines the config class for the rules API."""
from django.apps import AppConfig


class RulesApiConfig(AppConfig):
    """Defines the configuration for the rules API."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rules_api'
    verbose_name = 'Rules'

    def ready(self):
        """Set up rule signals when app is ready."""

        import rules_api.signals
