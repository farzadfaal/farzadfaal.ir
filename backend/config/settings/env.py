import environ
from .base import *  # noqa

ROOT_DIR = ROOT_DIR  # noqa

env = environ.Env(DEBUG=(bool, False))

environ.Env.read_env(ROOT_DIR / ".env")

DEBUG = env.bool("DJANGO_DEBUG", default=False)

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-bootstrap-only" if DEBUG else None,
)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=[],
)

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
    ),
}

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Django Vite
DJANGO_VITE = {
    "default": {
        "dev_mode": env("DJANGO_ENV", default="development") == "development",
        "dev_server_host": "localhost",
        "manifest_path": ROOT_DIR / "frontend" / "assets" / "manifest.json",
    }
}

# Wagtail
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000
WAGTAIL_SITE_NAME = "Farzad Faal"
WAGTAILADMIN_BASE_URL = env.str("WAGTAILADMIN_BASE_URL", default="localhost")
