"""
Django settings for jftf_core project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from sys import stdout
from .jftf_configuration import jftfXMLConfigManager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$gig*w@vdm0trjce(#*+=h$_%crcwor%b6*yg@6+bnh_eck!5r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'constance',
    'jftf_core_api',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    'drf_spectacular',
    'drf_api_logger',
    'django_filters',
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'jftf_core.urls'

JFTF_CORE_TEMPLATES_DIR = BASE_DIR / Path("jftf_core") / Path("templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [JFTF_CORE_TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jftf_core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'jftf_cmdb',
        'USER': 'jftf_dev',
        'PASSWORD': 'jftf_dev',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DRF_API_LOGGER_DATABASE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication backends

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Social account OAuth2 providers and various authentication configuration parameters

ACCOUNT_EMAIL_REQUIRED = True
LOGIN_URL = '/api/auth/login/'
LOGIN_REDIRECT_URL = '/api/'

REST_AUTH = {
    'SESSION_LOGIN': True,
    'USE_JWT': False,
}

# Django REST Framework settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

# CORS for React Admin JFTF-App

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'range',
]
CORS_EXPOSE_HEADERS = [
    'content-range',
    'content-disposition',
]

# Celery settings

CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'

# RabbitMQ credentials
RABBITMQ_USERNAME = 'jftf'
RABBITMQ_PASSWORD = 'jftf_development'

CELERY_BROKER_URL = f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@localhost:5672//'

# JFTF related configuration

JFTF_BASE_PATH = Path.home() / '.jftf' / 'config'

JFTF_AVAILABLE_RUNNERS = [
    'JftfDetachedRunner'
]

JFTF_CONFIGURATION_MANAGER = jftfXMLConfigManager

CONSTANCE_BACKEND = 'constance.backends.memory.MemoryBackend'

CONSTANCE_ADDITIONAL_FIELDS = {
    'appender_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ("consoleAppender", "consoleAppender"),
            ("fileAppender", "fileAppender"),
            ("syslogAppender", "syslogAppender"),
            ("multiAppender", "multiAppender"),
        )
    }],
    'log_level_select': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ("DEBUG", "DEBUG"),
            ("INFO", "INFO"),
            ("ERROR", "ERROR"),
        )
    }],
    'toggle_switch': ['django.forms.fields.ChoiceField', {
        'widget': 'django.forms.Select',
        'choices': (
            ("true", "true"),
            ("false", "false"),
        )
    }],
}

CONSTANCE_CONFIG = {
    'ip': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_CMDB_CFG, "ip"),
        f'IP Address of the database server (from {jftfXMLConfigManager.FILE_JFTF_CMDB_CFG})',
    ),
    'db_name': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_CMDB_CFG, "db_name"),
        f'Name of the database (from {jftfXMLConfigManager.FILE_JFTF_CMDB_CFG})',
    ),
    'username': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_CMDB_CFG, "username"),
        f'Username for database authentication (from {jftfXMLConfigManager.FILE_JFTF_CMDB_CFG})',
    ),
    'password': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_CMDB_CFG, "password"),
        f'Password for database authentication (from {jftfXMLConfigManager.FILE_JFTF_CMDB_CFG})',
    ),
    'api_hostname': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG, "api_hostname"),
        f'Hostname of the API server (from {jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG})',
    ),
    'api_port': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG, "api_port"),
        f'Port number of the API server (from {jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG})',
    ),
    'api_username': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG, "api_username"),
        f'Username for API authentication (from {jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG})',
    ),
    'api_password': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG, "api_password"),
        f'Password for API authentication (from {jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG})',
    ),
    'enable_debug': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "enable_debug"),
        f'Enable debugging (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'toggle_switch'
    ),
    'enable_logging': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "enable_logging"),
        f'Enable logging (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'toggle_switch'
    ),
    'syslog_server_ip': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "syslog_server_ip"),
        f'Syslog server IP address (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})',
    ),
    'daemon_app_id': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "daemon_app_id"),
        f'Daemon application ID (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})',
    ),
    'daemon_log_level': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "daemon_log_level"),
        f'Daemon log level (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'log_level_select'
    ),
    'daemon_appender': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "daemon_appender"),
        f'Daemon appender (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'appender_select'
    ),
    'test_app_id': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "test_app_id"),
        f'Test application ID (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})',
    ),
    'test_log_level': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "test_log_level"),
        f'Test log level (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'log_level_select'
    ),
    'test_appender': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "test_appender"),
        f'Test appender (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'appender_select'
    ),
    'control_app_id': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "control_app_id"),
        f'Control application ID (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})',
    ),
    'control_log_level': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "control_log_level"),
        f'Control log level (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'log_level_select'
    ),
    'control_appender': (
        jftfXMLConfigManager.get_value(jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG, "control_appender"),
        f'Control appender (from {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG})', 'appender_select'
    ),
    # Define other keys and descriptions in a similar manner
}

CONSTANCE_CONFIG_FIELDSETS = {
    f'Configuration for {jftfXMLConfigManager.FILE_JFTF_DAEMON_CFG}': (
        'api_hostname', 'api_port', 'api_username', 'api_password'),
    f'Configuration for {jftfXMLConfigManager.FILE_JFTF_CMDB_CFG}': ('ip', 'db_name', 'username', 'password'),
    f'Logger Configuration for {jftfXMLConfigManager.FILE_JFTF_LOGGER_CFG}': (
        'enable_debug', 'enable_logging', 'syslog_server_ip', 'daemon_app_id', 'daemon_log_level',
        'daemon_appender', 'test_app_id', 'test_log_level', 'test_appender', 'control_app_id',
        'control_log_level', 'control_appender'
    ),
}

# Email SMTP configuration parameters

JFTF_STATUS_EMAIL_ADDRESS = 'jftf.status@gmail.com'

ENABLE_EMAILS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = JFTF_STATUS_EMAIL_ADDRESS
EMAIL_HOST_PASSWORD = 'qcuejvmbbfqowizk'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

DEFAULT_FROM_EMAIL = JFTF_STATUS_EMAIL_ADDRESS
SERVER_EMAIL = JFTF_STATUS_EMAIL_ADDRESS
