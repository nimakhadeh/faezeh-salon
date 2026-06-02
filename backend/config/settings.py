# =============================================================================
# Faezeh Salon - Django Settings
# =============================================================================

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# Core Django Settings
# =============================================================================

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000").split(",")

# =============================================================================
# Application Definition
# =============================================================================

INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third Party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    "channels",
    "django_celery_beat",
    "django_celery_results",
    
    # Local Apps
    "apps.accounts",
    "apps.services",
    "apps.appointments",
    "apps.payments",
    "apps.wallet",
    "apps.loyalty",
    "apps.gallery",
    "apps.chat",
    "apps.survey",
    "apps.crm",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# =============================================================================
# Templates
# =============================================================================

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

# =============================================================================
# ASGI + Channels (WebSocket)
# =============================================================================

ASGI_APPLICATION = "config.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_HOST", "redis"), int(os.getenv("REDIS_PORT", "6379")))],
        },
    },
}

# =============================================================================
# WSGI
# =============================================================================

WSGI_APPLICATION = "config.wsgi.application"

# =============================================================================
# Database (PostgreSQL)
# =============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "faezeh_salon"),
        "USER": os.getenv("POSTGRES_USER", "faezeh_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
        "HOST": os.getenv("POSTGRES_HOST", "postgres"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# =============================================================================
# Password Validation
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =============================================================================
# Custom User Model
# =============================================================================

AUTH_USER_MODEL = "accounts.User"

# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# =============================================================================
# Static & Media Files
# =============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# =============================================================================
# Default Primary Key Field Type
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =============================================================================
# Django REST Framework
# =============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# =============================================================================
# JWT Settings
# =============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# =============================================================================
# CORS
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
]

CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# Celery Configuration
# =============================================================================

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# =============================================================================
# Zarinpal Configuration
# =============================================================================

ZARINPAL = {
    "MERCHANT_ID": os.getenv("ZARINPAL_MERCHANT_ID", ""),
    "SANDBOX": os.getenv("ZARINPAL_SANDBOX", "True").lower() == "true",
    "CALLBACK_URL": os.getenv("BACKEND_URL", "http://localhost:8000") + "/api/payments/verify/",
}

# =============================================================================
# Kavenegar Configuration
# =============================================================================

KAVENEGAR = {
    "API_KEY": os.getenv("KAVENEGAR_API_KEY", ""),
    "SENDER": os.getenv("KAVENEGAR_SENDER", ""),
}

# =============================================================================
# Cloudinary (Optional)
# =============================================================================

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

if CLOUDINARY_CLOUD_NAME:
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    INSTALLED_APPS += ["cloudinary_storage", "cloudinary"]

# =============================================================================
# Telegram Bot
# =============================================================================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_WEBHOOK_URL = os.getenv("TELEGRAM_WEBHOOK_URL", "")

# =============================================================================
# Salon Info
# =============================================================================

SALON_INFO = {
    "NAME": "سالن فائزه",
    "OWNER": "فائزه",
    "PHONE": "۰۹۳۹۹۵۴۵۱۱۳",
    "RAW_PHONE": "09399545113",
    "ADDRESSES": [
        "ستارخان کوچه ۱۲/۱",
        "عفیف‌آباد کوچه ۲۲",
    ],
    "INSTAGRAM": "@Baftmofaezeh",
    "BIO": "من فائزه‌ام، ۴ ساله که به‌صورت حرفه‌ای در زمینه بافت و اکستنشن مو فعالیت می‌کنم. مسیرم با علاقه به خلق استایل‌های خاص شروع شد، از بافت‌های ساده و روزمره تا کارهای پیشرفته و ژورنالی. هدف من این است که هر مشتری با حس اعتماد به نفس و زیبایی واقعی از سالن خارج بشه. کیفیت، دوام بالا و ظرافت کار برایم اولویت دارد.",
}
