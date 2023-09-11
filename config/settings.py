from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SECRET_KEY = "django-insecure-$cxbcol-eqyy_$ltpx#cmr1z+xmcaq+mi(2x)61*s-ylgkohrh"

DEBUG = True

ALLOWED_HOSTS = []

PROJECT_NAME = 'chatapp'

INSTALLED_APPS = [
    "app",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'daphne',
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'channels'
]

ASGI_APPLICATION = 'config.routing.application' 

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'app.middleware.TokenExpirationMiddleware'
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


BASE_DIR_DB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR_DB, 'mydatabase.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True



STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': [
       'rest_framework.permissions.IsAuthenticated',
   ],
   'DEFAULT_AUTHENTICATION_CLASSES': (
       'rest_framework.authentication.SessionAuthentication',
       'rest_framework.authentication.TokenAuthentication',
   )
   }

CORS_ALLOWED_ORIGINS = [
   "http://localhost:4200",
]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer", 
    },
}

AUTH_USER_MODEL = 'app.User'
