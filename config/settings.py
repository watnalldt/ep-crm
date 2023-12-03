"""
Django setting's for config project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
from pathlib import Path

import environ
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
    DEBUG_TOOLBAR=(bool, False),
)
env.read_env(str(BASE_DIR / ".env.development"))

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS: list[str] = env("ALLOWED_HOSTS")

DEBUG = env("DEBUG")
DEBUG_TOOLBAR = env("DEBUG_TOOLBAR")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


# Application definition

DJANGO_APPS = [
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "admin_auto_filters",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_extensions",
    "import_export",
    "rangefilter",
    "simple_history",
    "axes",
    "django_admin_logs",
    "django_browser_reload",
]


PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "clients.apps.ClientsConfig",
    "pages.apps.PagesConfig",
    "utilities.apps.UtilitiesConfig",
    "contracts.apps.ContractsConfig",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # https://whitenoise.evans.io/
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
# Enable the debug toolbar only in DEBUG mode.
if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "config.urls"

""" Custom User Authentication """
AUTH_USER_MODEL = "users.User"
LOGOUT_REDIRECT_URL = "users:login"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE")  # noqa F405


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_TZ = True

DATE_INPUT_FORMATS = ("%d/%m/%Y", "%d-%m-%Y")  # UK Date Setting


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Whitenoise
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MAX_UPLOAD_SIZE = "5242880"
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
GRAPPELLI_ADMIN_TITLE = "Energy Portfolio CRM Portal"
# Email Settings
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
# EMAIL_HOST = env("EMAIL_HOST")
# EMAIL_BACKEND = env("EMAIL_BACKEND")
# EMAIL_PORT = env("EMAIL_PORT")
# EMAIL_USE_TLS = env("EMAIL_USE_TLS")
# MAILJET_API_KEY = env("MAILJET_API_KEY")
# MAILJET_API_SECRET = env("MAILJET_API_SECRET")

ADMINS = [x.split(":") for x in env.list("DJANGO_ADMINS")]
# ADMINS = [("John", "john@example.com"), ("Mary", "mary@example.com")]
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Support <david@energyportfolio.co.uk>",
)

# # https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

AXES_FAILURE_LIMIT = 3  # How many times a user can fail to log in
AXES_COOLOFF_TIME = timedelta(minutes=10)  # How long before a user can fail to log in
AXES_RESET_ON_SUCCESS = True  # Reset failed login attempts after successful login
AXES_LOCKOUT_TEMPLATE = "account_locked.html"
AXES_RESET_COOL_OFF_ON_FAILURE_DURING_LOCKOUT = False
AXES_LOCKOUT_PARAMETERS = [
    [
        "username",
    ]
]
