from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Detección de entorno ---
RAILWAY_ENVIRONMENT = os.getenv('RAILWAY_ENVIRONMENT_NAME')
IS_PRODUCTION = RAILWAY_ENVIRONMENT == 'production'

# --- Seguridad / entorno ---
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-*q(juvh&o%giq7*4rns!$f+h$^)n_i-^3yg-5ej7_&1s2rlz4m")
DEBUG = os.getenv("DEBUG", "True" if not IS_PRODUCTION else "False") == "True"

# Configuración de hosts según entorno
if IS_PRODUCTION:
    ALLOWED_HOSTS = [
        "portafolio-zetzer-production.up.railway.app",
        ".railway.app",  # Para subdominios de Railway
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://portafolio-zetzer-production.up.railway.app",
    ]
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
    CSRF_TRUSTED_ORIGINS = []

# Permitir hosts adicionales desde variable de entorno
additional_hosts = os.getenv("ALLOWED_HOSTS", "").split(",")
if additional_hosts and additional_hosts != [""]:
    ALLOWED_HOSTS.extend(additional_hosts)

additional_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
if additional_csrf and additional_csrf != [""]:
    CSRF_TRUSTED_ORIGINS.extend(additional_csrf)

# --- Apps ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # WhiteNoise: debe ir ANTES de staticfiles
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Tus apps
    "portfolio_projects",
    "auth_users",
    "core",
    # Media en Spaces
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
if IS_PRODUCTION:
    # En producción, usar PostgreSQL de Railway
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # En desarrollo, usar SQLite local
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# También permitir usar PostgreSQL en desarrollo si se especifica
if os.getenv("USE_POSTGRES_LOCAL") == "True":
    DATABASES = {
        "default": dj_database_url.config(
            default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
            conn_max_age=600,
            ssl_require=False,  # SSL False para desarrollo
        )
    }

# --- Validadores de contraseña ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- I18N ---
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# --- Static Files (WhiteNoise) ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Media Files ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Configuración de DigitalOcean Spaces
AWS_ACCESS_KEY_ID = os.getenv("DO_SPACES_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("DO_SPACES_SECRET")
AWS_STORAGE_BUCKET_NAME = os.getenv("DO_SPACES_BUCKET")
AWS_S3_REGION_NAME = os.getenv("DO_SPACES_REGION")
AWS_S3_ENDPOINT_URL = os.getenv("DO_SPACES_ENDPOINT")
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

# Usar Spaces solo si todas las credenciales están disponibles
USE_SPACES = all([
    AWS_ACCESS_KEY_ID, 
    AWS_SECRET_ACCESS_KEY, 
    AWS_STORAGE_BUCKET_NAME, 
    AWS_S3_REGION_NAME,
    AWS_S3_ENDPOINT_URL
])

if USE_SPACES:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/"
    print(f"✅ Usando DigitalOcean Spaces: {AWS_STORAGE_BUCKET_NAME}")
else:
    # Fallback a almacenamiento local
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    print("⚠️ Usando almacenamiento local para media files")

# --- Configuración de seguridad ---
if IS_PRODUCTION:
    # Configuración HTTPS para producción
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # Configuración para desarrollo
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# --- Logging ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO' if IS_PRODUCTION else 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Información de debug ---
if DEBUG:
    print(f"🔧 Environment: {'Production' if IS_PRODUCTION else 'Development'}")
    print(f"🔧 Database: {'PostgreSQL' if 'postgres' in str(DATABASES['default'].get('ENGINE', '')) or os.getenv('DATABASE_URL') else 'SQLite'}")
    print(f"🔧 Debug: {DEBUG}")
    print(f"🔧 Allowed Hosts: {ALLOWED_HOSTS}")