from django.apps import AppConfig


class JftfCoreApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jftf_core_api'

    def ready(self):
        import jftf_core_api.signals
