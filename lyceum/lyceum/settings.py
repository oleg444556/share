from pathlib import Path

from django.utils.translation import gettext_lazy as _
import environ


BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, "fake_secret_key"),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    DJANGO_ALLOW_REVERSE=(bool, True),
    DJANGO_MAIL=(str, "example@bk.ru"),
)
environ.Env.read_env(BASE_DIR / ".env")

TRUE_DEF = ("", "true", "True", "yes", "YES", "1", "y")

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = True if str(env("DJANGO_DEBUG")) in TRUE_DEF else False

ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

ALLOW_REVERSE = True if str(env("DJANGO_ALLOW_REVERSE")) in TRUE_DEF else False

DJANGO_MAIL = env("DJANGO_MAIL")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cleanup.apps.CleanupConfig",
    "sorl.thumbnail",
    "ckeditor",
    "core.apps.CoreConfig",
    "about.apps.AboutConfig",
    "download.apps.DownloadConfig",
    "catalog.apps.CatalogConfig",
    "homepage.apps.HomepageConfig",
    "feedback.apps.FeedbackConfig",
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

if ALLOW_REVERSE:
    MIDDLEWARE.append("lyceum.middleware.RussianWordsReverseMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = "lyceum.urls"

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

WSGI_APPLICATION = "lyceum.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": [
            ["Bold", "Italic"],
            [
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
            ],
        ],
        "height": 100,
        "width": 500,
    },
}


LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
DEFAULT_CHARSET = "utf-8"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True
LOCALE_PATHS = [BASE_DIR / "locale"]

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_prod"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_mail"
