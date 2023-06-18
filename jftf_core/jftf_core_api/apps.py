from django.apps import AppConfig
from pathlib import Path
from .jftf_configuration import jftfXMLConfigManager


class JftfCoreApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jftf_core_api'

    def ready(self):
        config_dir = Path.home() / '.jftf' / 'config'
        jftf_config_manager = jftfXMLConfigManager(config_dir)
        jftf_config_manager.check_integrity()
