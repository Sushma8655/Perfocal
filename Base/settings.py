"""
Django settings for Base project.

Generated by 'django-admin startproject' using Django 3.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-rv38&v)x$8&=ikbd$r9@pc$ku7geny^&+$%4p)zkgc2in8n89t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perfocal',
    'maintenance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf',
            ],
        },
    },
]

WSGI_APPLICATION = 'Base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

local = 0

if local == 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'neha1626',
            'HOST': 'localhost'
        }
    }
if local == 1:
    LOCAL_POSTGRES = 'postgres://a9s0283608990e4f378eeddcc917c2428b687acf4a3:a9s22ecab00340ebe65b7bdba7a1df5568c8f8262e4@pod555779-psql-master-alias.node.dc1.a9ssvc:5432/pod555779'
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(default=LOCAL_POSTGRES)

if local == 2:
    LOCAL_POSTGRES = 'postgres://a9sbd76381f99c520c02aa55a58fcb702fdfaa6c124:a9s64fe547514df8abb1d9d368a1b06d280bdb7af04@pod555779-psql-master-alias.node.dc1.a9ssvc:5432/pod555779'
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(default=LOCAL_POSTGRES)


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

os.environ['MINDSPHERE_CLIENT_ID'] = 'preindev-perfocal-v1.0.0'
os.environ['MINDSPHERE_CLIENT_SECRET'] = '8nfML0XtSTqc6B8My5NAToGIxoYyTvLPeHiiE4XrLGh'
os.environ['MINDSPHERE_TENANT'] = 'preindev'
os.environ['MDSP_HOST_TENANT'] = 'preindev'
os.environ['MDSP_USER_TENANT'] = 'preindev'
os.environ['MDSP_OS_VM_APP_NAME'] = 'perfocal'
os.environ['MDSP_OS_VM_APP_VERSION'] = 'v1.0.0'
os.environ['MDSP_KEY_STORE_CLIENT_ID'] = 'preindev-perfocal-v1.0.0'
os.environ['MDSP_KEY_STORE_CLIENT_SECRET'] = '8nfML0XtSTqc6B8My5NAToGIxoYyTvLPeHiiE4XrLGh'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'

# STATIC_PATH = os.path.join(BASE_DIR, 'Base/static')
#
# STATIC_URL = '/static/' # You may find this is already defined as such.
#
# STATICFILES_DIRS = (
#     STATIC_PATH,
# )
# STATIC_URL = '/static/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
