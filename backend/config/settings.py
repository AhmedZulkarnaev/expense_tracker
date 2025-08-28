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
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # Local apps
    "users.apps.UsersConfig",
    "expenses.apps.ExpensesConfig",
]

# ──────────────────────────────
# 🧱 Middleware
# ──────────────────────────────

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
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

FRONTEND_DIR = BASE_DIR / "frontend"
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = BASE_DIR.parent / "frontend"

TEMPLATES[0]["DIRS"] = [FRONTEND_DIR]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
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
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# ──────────────────────────────
# мета-информация схемы
# ──────────────────────────────

SPECTACULAR_SETTINGS = {
    "TITLE": "Expense Tracker API",
    "DESCRIPTION": "Учёт доходов/расходов: аутентификация, операции, отчёты и экспорт.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
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
STATICFILES_DIRS = [FRONTEND_DIR]

# ──────────────────────────────
# 🔑 PK по умолчанию
# ──────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
