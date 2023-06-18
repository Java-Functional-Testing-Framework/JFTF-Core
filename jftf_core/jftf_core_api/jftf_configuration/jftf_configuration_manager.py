import os
import logging
from lxml import etree


class XMLConfigManager:
    FILE_JFTF_CMDB_CFG = 'jftf_cmdb_cfg.xml'
    FILE_JFTF_DAEMON_CFG = 'jftf_daemon_cfg.xml'
    FILE_JFTF_LOGGER_CFG = 'jftf_logger_cfg.xml'

    ELEMENTS_JFTF_CMDB_CFG = {
        'ip': 'credentials/ip',
        'db_name': 'credentials/db_name',
        'username': 'credentials/username',
        'password': 'credentials/password',
    }

    ELEMENTS_JFTF_DAEMON_CFG = {
        'api_hostname': 'jftf_core_config/api_hostname',
        'api_port': 'jftf_core_config/api_port',
        'api_username': 'jftf_core_config/api_username',
        'api_password': 'jftf_core_config/api_password',
    }

    ELEMENTS_JFTF_LOGGER_CFG = {
        'enable_debug': 'behaviour/enable_debug',
        'enable_logging': 'behaviour/enable_logging',
        'syslog_server_ip': 'ip/syslog_server_ip',
        'daemon_app_id': 'daemon_ctx_info/app_id',
        'daemon_log_level': 'daemon_ctx_info/log_level',
        'daemon_appender': 'daemon_ctx_info/appender',
        'test_app_id': 'jftf_test_ctx_info/app_id',
        'test_log_level': 'jftf_test_ctx_info/log_level',
        'test_appender': 'jftf_test_ctx_info/appender',
        'control_app_id': 'jftf_control_app_info/app_id',
        'control_log_level': 'jftf_control_app_info/log_level',
        'control_appender': 'jftf_control_app_info/appender',
    }

    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.logger = self._setup_logger()

    def _setup_logger(cls):
        """
        Set up the logger for the XMLConfigManager class.
        """
        logger = logging.getLogger("jftfXMLConfigManager")
        logger.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(console_handler)

        return logger

    def _get_file_path(self, file_name):
        return os.path.join(self.config_dir, file_name)

    def _load_xml_file(self, file_name):
        file_path = self._get_file_path(file_name)
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(file_path, parser)
        return tree

    def _save_xml_file(self, file_name, tree):
        file_path = self._get_file_path(file_name)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

    def check_integrity(self):
        for file_name in [self.FILE_JFTF_CMDB_CFG, self.FILE_JFTF_DAEMON_CFG, self.FILE_JFTF_LOGGER_CFG]:
            file_path = self._get_file_path(file_name)
            if not os.path.isfile(file_path):
                self.logger.error(f"Configuration file '{file_name}' not found.")
                raise FileNotFoundError(f"Configuration file '{file_name}' not found.")

            try:
                tree = self._load_xml_file(file_name)
                root = tree.getroot()

                if file_name == self.FILE_JFTF_CMDB_CFG:
                    elements = self.ELEMENTS_JFTF_CMDB_CFG
                elif file_name == self.FILE_JFTF_DAEMON_CFG:
                    elements = self.ELEMENTS_JFTF_DAEMON_CFG
                elif file_name == self.FILE_JFTF_LOGGER_CFG:
                    elements = self.ELEMENTS_JFTF_LOGGER_CFG
                else:
                    self.logger.error(f"Invalid configuration file '{file_name}'.")
                    raise ValueError(f"Invalid configuration file '{file_name}'.")

                for key, path in elements.items():
                    element = root.find(path)
                    if element is None:
                        self.logger.error(f"Missing element '{path}' in '{file_name}'.")
                        raise ValueError(f"Missing element '{path}' in '{file_name}'.")

            except etree.ParseError as e:
                self.logger.error(f"Invalid XML format in '{file_name}': {e}")
                raise ValueError(f"Invalid XML format in '{file_name}': {e}")

    def get_value(self, file_name, key):
        if file_name == self.FILE_JFTF_CMDB_CFG:
            elements = self.ELEMENTS_JFTF_CMDB_CFG
        elif file_name == self.FILE_JFTF_DAEMON_CFG:
            elements = self.ELEMENTS_JFTF_DAEMON_CFG
        elif file_name == self.FILE_JFTF_LOGGER_CFG:
            elements = self.ELEMENTS_JFTF_LOGGER_CFG
        else:
            self.logger.error(f"Invalid configuration file '{file_name}'.")
            raise ValueError(f"Invalid configuration file '{file_name}'.")

        if key not in elements:
            self.logger.error(f"Invalid key '{key}' for configuration file '{file_name}'.")
            raise ValueError(f"Invalid key '{key}' for configuration file '{file_name}'.")

        tree = self._load_xml_file(file_name)
        element = tree.find(elements[key])

        if element is not None:
            return element.text
        else:
            self.logger.warning(f"Missing element '{elements[key]}' in '{file_name}'.")
            # Handle the case when the element is not found
            return None

    def get_config(self, file_name):
        tree = self._load_xml_file(file_name)
        config = {}

        if file_name == self.FILE_JFTF_CMDB_CFG:
            elements = self.ELEMENTS_JFTF_CMDB_CFG
        elif file_name == self.FILE_JFTF_DAEMON_CFG:
            elements = self.ELEMENTS_JFTF_DAEMON_CFG
        elif file_name == self.FILE_JFTF_LOGGER_CFG:
            elements = self.ELEMENTS_JFTF_LOGGER_CFG
        else:
            self.logger.error(f"Invalid configuration file '{file_name}'.")
            raise ValueError(f"Invalid configuration file '{file_name}'.")

        for key, path in elements.items():
            element = tree.find(path)
            if element is not None:
                config[key] = element.text
            else:
                self.logger.warning(f"Missing element '{path}' in '{file_name}'.")
                # Handle the case when the element is not found

        return config

    def set_value(self, file_name, key, value):
        if file_name == self.FILE_JFTF_CMDB_CFG:
            elements = self.ELEMENTS_JFTF_CMDB_CFG
        elif file_name == self.FILE_JFTF_DAEMON_CFG:
            elements = self.ELEMENTS_JFTF_DAEMON_CFG
        elif file_name == self.FILE_JFTF_LOGGER_CFG:
            elements = self.ELEMENTS_JFTF_LOGGER_CFG
        else:
            raise ValueError(f"Invalid configuration file '{file_name}'.")

        tree = self._load_xml_file(file_name)
        root = tree.getroot()

        if key in elements:
            path = elements[key]
            element = root.xpath(path)
            if element:
                element[0].text = value
                self._save_xml_file(file_name, tree)
            else:
                raise ValueError(f"Element '{path}' not found in '{file_name}'.")
        else:
            raise ValueError(f"Invalid key '{key}' for configuration file '{file_name}'.")

    def set_config(self, file_name, updates):
        tree = self._load_xml_file(file_name)

        if file_name == self.FILE_JFTF_CMDB_CFG:
            elements = self.ELEMENTS_JFTF_CMDB_CFG
        elif file_name == self.FILE_JFTF_DAEMON_CFG:
            elements = self.ELEMENTS_JFTF_DAEMON_CFG
        elif file_name == self.FILE_JFTF_LOGGER_CFG:
            elements = self.ELEMENTS_JFTF_LOGGER_CFG
        else:
            self.logger.error(f"Invalid configuration file '{file_name}'.")
            raise ValueError(f"Invalid configuration file '{file_name}'.")

        root = tree.getroot()

        for key, path in elements.items():
            if key in updates:
                value = updates[key]
                element = root.xpath(path)
                if element:
                    element[0].text = value
                else:
                    parent = root.xpath('/'.join(path.split('/')[:-1]))
                    if parent:
                        new_element = etree.SubElement(parent[0], key)
                        new_element.text = value

        self._save_xml_file(file_name, tree)
        self.logger.info(f"Configuration '{file_name}' has been updated.")
