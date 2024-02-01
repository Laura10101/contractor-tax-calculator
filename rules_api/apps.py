from django.apps import AppConfig


class RulesApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rules_api'
    verbose_name = 'Rules'

    def ready(self):
        import rules_api.signals
