from pathlib import Path
from decouple import config

# ──────────────────────────────
# 🔧 Базовые настройки проекта
# ──────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-dev-key")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = []

# ──────────────────────────────
# 📦 Установленные приложения
# ──────────────────────────────

INSTALLED_APPS = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    # Local apps
    "users.apps.UsersConfig",
    "expenses.apps.ExpensesConfig",
]

# ──────────────────────────────
# 🧱 Middleware
# ──────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ──────────────────────────────
# 🌐 URL & WSGI
# ──────────────────────────────

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ──────────────────────────────
# 🖼️ Шаблоны
# ──────────────────────────────

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

# ──────────────────────────────
# 🗃️ База данных
# ──────────────────────────────

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", default="expense_db"),
        "USER": config("POSTGRES_USER", default="expense_user"),
        "PASSWORD": config("POSTGRES_PASSWORD", default="expense_pass"),
        "HOST": "db",
        "PORT": 5432,
    }
}

# ──────────────────────────────
# 🔐 Аутентификация и пользователи
# ──────────────────────────────

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────
# 🧪 DRF настройки
# ──────────────────────────────

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ──────────────────────────────
# 🌍 Локализация и часовой пояс
# ──────────────────────────────

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────
# 📂 Статика
# ──────────────────────────────

STATIC_URL = "static/"

# ──────────────────────────────
# 🔑 PK по умолчанию
# ──────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
