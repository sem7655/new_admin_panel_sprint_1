"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from split_settings.tools import include
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = ['127.0.0.1']


# Application definition
include(
    "components/installedapp.py",
)
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

include(
    "components/database.py",
)

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
include(
    "components/passw.py",
)

# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "static")
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
LOCALE_PATHS = ['movies/locale']
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'