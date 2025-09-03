from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

# --- Rutas base ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Seguridad / entorno ---
SECRET_KEY = 'django-insecure-*q(juvh&o%giq7*4rns!+hCopy-Item)n_i-^3yg-5ej7_&1s2rlz4m'
DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if not DEBUG else ["*"]
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # WhiteNoise antes de staticfiles
    "django.contrib.staticfiles",
    # Apps propias
    "portfolio_projects",
    "auth_users",
    "core",
    # Soporte para Spaces
    "storages",
]

# --- Middleware ---
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

ROOT_URLCONF = "portfolio_project.urls"
WSGI_APPLICATION = "portfolio_project.wsgi.application"

# --- Templates ---
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

# --- Base de datos ---
if DEBUG:
    # SQLite para desarrollo local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # PostgreSQL en producción (Railway)
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        DATABASES = {
            "default": dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                ssl_require=True,
            )
        }
    else:
        # fallback a SQLite si no hay URL
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

# --- Validadores de contraseña ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Idioma y zona horaria ---
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Archivos multimedia ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- DigitalOcean Spaces ---
AWS_ACCESS_KEY_ID = os.getenv("DO_SPACES_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("DO_SPACES_SECRET")
AWS_STORAGE_BUCKET_NAME = os.getenv("DO_SPACES_BUCKET")
AWS_S3_REGION_NAME = os.getenv("DO_SPACES_REGION")
AWS_S3_ENDPOINT_URL = os.getenv("DO_SPACES_ENDPOINT")  # Debe ser https://sfo3.digitaloceanspaces.com

AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

if all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME]):
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com/"

# --- HTTPS detrás de proxy (Railway) ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
