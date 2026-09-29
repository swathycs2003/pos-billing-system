"""
Django settings for config project.
Modified for production deployment on Render.
"""

import os
from pathlib import Path
import dj_database_url  # Fast database string parsing tool

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------- PRODUCTION ENVIRONMENT CHECKS -----------------
# Render passes an environment variable called 'RENDER' once it is live
IS_PRODUCTION = os.environ.get('RENDER', 'False') == 'True'

# SECURITY WARNING: keep the secret key used in production secret!
if IS_PRODUCTION:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
else:
    SECRET_KEY = 'django-insecure-#odcdy(0ywl=())8!98u_=8^#!39p-trckn1461!91&lzkyh05'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION

# Allow local addresses and your upcoming Render domain
ALLOWED_HOSTS = ['*']
# -----------------------------------------------------------------

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps:
    'management',
    'billing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <-- CRITICAL: Put WhiteNoise directly here
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Uses dj-database-url to automatically read the 'DATABASE_URL' environment variable on Render.
# Falls back to local SQLite database if running on your machine.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Absolute directory destination where collectstatic gathers files for deployment
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise storage engine configurations to compress assets for faster loads
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/portal-router/'
