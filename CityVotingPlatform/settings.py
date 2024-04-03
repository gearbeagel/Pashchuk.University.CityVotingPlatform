import sys
from pathlib import Path
import environ

from django.contrib import staticfiles
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv('.env')
secret_key: str = os.getenv('secret_key')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['cityvoting.azurewebsites.net', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://cityvoting.azurewebsites.net']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'city_voting_registration',
    'city_map',
    'homepage',
    'voting',
    'user_submissions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'CityVotingPlatform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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
storage_key: str = os.getenv('storage_key')
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_config")
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        'BACKEND': 'storages.backends.azure_storage.AzureStorage',
        'AZURE_ACCOUNT_NAME': 'cityvotingstorageaccount',
        'AZURE_ACCOUNT_KEY': storage_key,
        'AZURE_CONTAINER': 'profpicscont',
    },
}

AZURE_ACCOUNT_NAME = 'cityvotingstorageaccount'
AZURE_ACCOUNT_KEY = storage_key
AZURE_CONTAINER = 'profpicscont'

STATIC_HOST = os.environ.get("DJANGO_STATIC_HOST", "")
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static", ]

WSGI_APPLICATION = 'CityVotingPlatform.wsgi.application'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Database
db_password: str = os.getenv('db_password')

environ.Env.DB_SCHEMES['mssql'] = 'mssql'
env = environ.Env(DEBUG=(bool, False))
DEFAULT_DATABASE_URL = (
    f'mssql://krato:{db_password}@citivoting-db-server.database.windows.net/cityvoting_db?driver=ODBC'
    '+Driver+17+for+SQL+Server')

DATABASE_URL = os.environ.get('DATABASE_URL', DEFAULT_DATABASE_URL)
os.environ['DJANGO_DATABASE_URL'] = DATABASE_URL.format(**os.environ)

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': env.db('DJANGO_DATABASE_URL', default=DEFAULT_DATABASE_URL)
    }
# Password validation

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Site ID
SITE_ID = 4

# Social authentication settings
SOCIALACCOUNT_LOGIN_ON_GET = True

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Redirect URLs after login and logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = '/'
# Welcome email configurations
passwrd: str = os.getenv('passwrd')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'vebvebenko@gmail.com'
EMAIL_HOST_PASSWORD = passwrd
EMAIL_USE_TLS = True
