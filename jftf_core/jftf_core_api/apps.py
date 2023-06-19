from django.apps import AppConfig
from django.conf import settings


class JftfCoreApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jftf_core_api'

    def ready(self):
        import jftf_core_api.signals
        settings.JFTF_CONFIGURATION_MANAGER.check_integrity()
