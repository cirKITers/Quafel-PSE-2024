"""
Django settings for quafelweb project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Add .env variables anywhere before SECRET_KEY
dotenv_file = (BASE_DIR.parent / ".env_secret").resolve()
if dotenv_file.is_file():
    for line in dotenv_file.read_text().splitlines():
        if line.startswith("#"): continue
        line = line.strip().replace(' ', '')
        key, value = line.split("=", 2)
        os.environ[key] = value
else:
    raise RuntimeError("The .env_secret file is not present, get the .env_secret file from an admin")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g715+$i5t@rzbi)-ktamejq27%@g*os=-i3s67c$5hofs6x-aj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'quafelweb',

    # libs
    'authlib',
    'quafel_simulators',

    # apps
    'account_controller',
    'hardware_controller',
    'simulation_controller',
    'simulation_data',
    'simulation_view',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'quafelweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', 'templatetags'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

STATICFILES_DIRS = [
    "static",
]

WSGI_APPLICATION = 'quafelweb.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "database",
        "USER": "postgres",
        "PASSWORD": "postgresql",
        "HOST": "postgres",
        "PORT": "5432",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


OPENID_SECRET = os.environ["OPENID_KIT_SECRET_KEY"]
OPENID_CLIENT_ID = os.environ["OPENID_KIT_CLIENT_ID"]

OPENID_CONF_URL = "https://oidc.scc.kit.edu/auth/realms/kit/.well-known/openid-configuration"
OPENID_CLIENT_IDENT = 'email'

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
