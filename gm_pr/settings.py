#
# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django settings for gm_pr project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from gm_pr.settings_projects import *
import configparser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# You can override some settings with a "settings.ini" file project root
# directory:
#
# [backend]
# BROKER_URL="mybrokerurl"
# ...
config = configparser.ConfigParser()
config.read(os.sep.join([BASE_DIR, "settings.ini"]))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nny#i^ey9pbud@86s9p55r4k2fbd_0e+1#@h9+5z$+3nk2i&ml'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Either modify the ALLOWED_HOSTS directly in this file:
# ex: ALLOWED_HOSTS = ["10.0.0.2", "10.0.0.3"]
# or as an environment variable
# ex: env GM_PR_ALLOWED_HOSTS="10.0.0.2,10.0.0.3"
ALLOWED_HOSTS = os.environ.get('GM_PR_ALLOWED_HOSTS', '*').split(",")


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djcelery',
    'import_export',
    'gm_pr',
    'web',
    'bot',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'gm_pr.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'gm_pr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'rw', 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR+'/web/static/'

CELERY_ACCEPT_CONTENT = ['json', 'yaml', 'pickle']

CELERY_IMPORTS = ("bot.tasks", "gm_pr.prfetcher")
BROKER_URL = config.get('backend', 'BROKER_URL',
                        fallback='amqp://gm_pr:gm_pr@localhost:5672/gm_pr')
CELERY_RESULT_BACKEND = 'amqp'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'rw', 'gm_pr.log'),
            'maxBytes': 10000000,
            'backupCount': 5,
            'formatter' : 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'gm_pr': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
        },
    },
}
