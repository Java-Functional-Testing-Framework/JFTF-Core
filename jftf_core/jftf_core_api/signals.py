from django.dispatch import receiver
from constance.signals import config_updated
from django.conf import settings
from logging import getLogger

logger = getLogger(__name__)


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    if new_value is not None:
        file_name = None
        for mapping_key, fields in settings.CONSTANCE_CONFIG_FIELDSETS.items():
            if key in fields:
                file_name = mapping_key.split('Configuration for ')[1]
                break

        if file_name is not None:
            try:
                config_manager = settings.JFTF_CONFIGURATION_MANAGER
                current_value = config_manager.get_value(file_name, key)
                if current_value != new_value:
                    config_manager.set_value(file_name, key, new_value)
                    logger.info(
                        f"Updated configuration - Key: {key}, New Value: {new_value}, Configuration file: {file_name}")
                else:
                    logger.warning(
                        f"Skipped configuration update - Key: {key}, Configuration file: {file_name} . Existing value "
                        "is already equal to the new value.")
            except Exception as e:
                logger.error(
                    f"Failed to update configuration - Key: {key}, Configuration file: {file_name}, Error: {e}")
        else:
            logger.error(f"Failed to update configuration - Key: {key}. File mapping not found.")
