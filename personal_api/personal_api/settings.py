import logging.config
import os

from decouple import config
from django.utils.log import DEFAULT_LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS').replace('"', '').split(';')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'django_extensions',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personal_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    }
]

WSGI_APPLICATION = 'personal_api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.MinimumLengthValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        )
    },
]

CORS_ALLOW_METHODS = (
    # 'DELETE',
    # 'GET',
    # 'OPTIONS',
    # 'PATCH',
    # 'POST',
    # 'PUT',
    '*',
)

CORS_ORIGIN_ALLOW_ALL = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE', default='UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC_URL = 'https://domain.app/static/'
STATIC_URL = '/static/'

# Logging configuration, as JSON, to stdout.
LOG_LEVEL = config('LOG_LEVEL', default='INFO')
LOG_VARS = config('LOG_VARS')
JSON_LOGS = config('JSON_LOGS', default=False, cast=bool)
if JSON_LOGS:
    log_format = ' '.join(
        ['%({0:s})'.format(variable) for variable in LOG_VARS.split()]
    )
else:
    log_format = ''
    for index, variable in enumerate(LOG_VARS.split()):
        if variable != 'asctime':
            log_format += ' '
        log_format += f'%({variable})s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {'level': LOG_LEVEL, 'handlers': ['console']},
    'formatters': {
        'default': {'format': log_format, 'datefmt': '%Y%m%d.%H%M%S'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
            'formatter': 'default',
        }
    },
    'loggers': {
        # default for all undefined Python modules
        '': {'level': 'WARNING', 'handlers': ['console']}
    },
}

if JSON_LOGS:
    LOGGING['formatters']['default'][
        'class'
    ] = 'pythonjsonlogger.jsonlogger.JsonFormatter'

# Add runserver request logging back in
for key in ['formatters', 'handlers', 'loggers']:
    LOGGING[key]['django.server'] = DEFAULT_LOGGING[key]['django.server']
logging.config.dictConfig(LOGGING)

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination' '.LimitOffsetPagination'
    ),
    'PAGE_SIZE': 30,
}

# celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_BACKEND = config('CELERY_BROKER_BACKEND')

# This config allows tasks run instantly, without needing brokers
# CELERY_TASK_ALWAYS_EAGER = True

if CELERY_BROKER_BACKEND == 'rabbitmq':
    CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}'.format(
        user=config('RABBITMQ_USER'),
        password=config('RABBITMQ_PASSWORD'),
        host=config('RABBITMQ_ADDRESS'),
        port=config('RABBITMQ_PORT'),
    )
else:
    raise Exception(f'Unknown CELERY_BROKER_BACKEND={CELERY_BROKER_BACKEND}')
