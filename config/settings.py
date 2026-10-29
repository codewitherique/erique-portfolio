
import os
from pathlib import Path

import cloudinary
import dj_database_url
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================================================
# BASIC SETTINGS
# ==================================================

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

IS_RENDER = bool(os.environ.get("RENDER"))
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()

if IS_RENDER:
    DEBUG = False

# ==================================================
# HOSTS AND CSRF
# ==================================================

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=Csv(),
)

if IS_RENDER:
    ALLOWED_HOSTS.extend(
        host for host in [
            RENDER_HOST,
            "erique-portfolio-2.onrender.com",
        ]
        if host and host not in ALLOWED_HOSTS
    )

CSRF_TRUSTED_ORIGINS = [
    "https://erique-portfolio-2.onrender.com",
]

if RENDER_HOST:
    render_origin = f"https://{RENDER_HOST}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

# ==================================================
# APPLICATIONS
# ==================================================

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "core",
]

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==================================================
# DATABASE
# ==================================================

DATABASE_URL = config("DATABASE_URL", default="").strip()

if IS_RENDER:
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is missing from Render Environment Variables."
        )

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
elif DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="erique_db"),
            "USER": config("DB_USER", default="erique_db_user"),
            "PASSWORD": config("DB_PASSWORD", default=""),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
            "CONN_MAX_AGE": 60,
        }
    }

# ==================================================
# PASSWORD VALIDATION
# ==================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# ==================================================
# LANGUAGE AND TIME
# ==================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Dar_es_Salaam"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ==================================================
# MEDIA FILES
# ==================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==================================================
# CLOUDINARY
# ==================================================

CLOUDINARY_CLOUD_NAME = config(
    "CLOUDINARY_CLOUD_NAME",
    default="",
).strip()

CLOUDINARY_API_KEY = config(
    "CLOUDINARY_API_KEY",
    default="",
).strip()

CLOUDINARY_API_SECRET = config(
    "CLOUDINARY_API_SECRET",
    default="",
).strip()

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": CLOUDINARY_CLOUD_NAME,
    "API_KEY": CLOUDINARY_API_KEY,
    "API_SECRET": CLOUDINARY_API_SECRET,
}

# Explicitly configure the Cloudinary SDK
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

# Fail early on Render if credentials are missing.
# Never print the API secret in logs.
if IS_RENDER:
    missing_cloudinary_settings = [
        name
        for name, value in [
            ("CLOUDINARY_CLOUD_NAME", CLOUDINARY_CLOUD_NAME),
            ("CLOUDINARY_API_KEY", CLOUDINARY_API_KEY),
            ("CLOUDINARY_API_SECRET", CLOUDINARY_API_SECRET),
        ]
        if not value
    ]

    if missing_cloudinary_settings:
        raise RuntimeError(
            "Missing Render environment variables: "
            + ", ".join(missing_cloudinary_settings)
        )

# ==================================================
# SECURITY
# ==================================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    if IS_RENDER:
        SECURE_HSTS_SECONDS = 31536000
        SECURE_HSTS_INCLUDE_SUBDOMAINS = True
        SECURE_HSTS_PRELOAD = True

# ==================================================
# JAZZMIN ADMIN
# ==================================================

JAZZMIN_SETTINGS = {
    "site_title": "Erique Portfolio Administration",
    "site_header": "Erique Developer Portfolio",
    "site_brand": "Erique",
    "welcome_sign": "Website Content Management",
    "copyright": "Erique",
    "search_model": ["core.Project"],
    "order_with_respect_to": [
        "core.SiteSettings",
        "core.Education",
        "core.Skill",
        "core.Project",
        "core.Referee",
        "core.ContactMessage",
    ],
    "icons": {
        "core.SiteSettings": "fas fa-cog",
        "core.Education": "fas fa-graduation-cap",
        "core.Skill": "fas fa-code",
        "core.Project": "fas fa-folder-open",
        "core.Referee": "fas fa-user-tie",
        "core.ContactMessage": "fas fa-envelope",
        "auth.User": "fas fa-user",
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "navbar": "navbar-dark",
    "sidebar": "sidebar-dark-primary",
    "accent": "accent-primary",
}

# ==================================================
# LOGGING
# ==================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
