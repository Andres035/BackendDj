# C:\Users\benit\Downloads\Tienda-Online-main\BackendDj\main\settings.py
import os
from pathlib import Path
from datetime import timedelta
import cloudinary
from decouple import config
import dj_database_url

from dotenv import load_dotenv
load_dotenv()
from django.db import connections


# gunicorn main.wsgi:application
# BASE DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta
SECRET_KEY = os.getenv('SECRET_KEY', 'valor-por-defecto-para-desarrollo')
# Modo debug
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ['*'] if DEBUG else ['themause.onrender.com']
ALLOWED_HOSTS = ['backenddj-1.onrender.com', 'localhost', '127.0.0.1']
  
#   https://backenddj-1.onrender.com
# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
     'cloudinary_storage',
    'django.contrib.staticfiles',

    # Terceros
    
    'cloudinary',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',

    # Apps locales
    'users',
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs
ROOT_URLCONF = 'main.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# base datos maestro
""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'ERMDtLlspadbrHFCEySgYIaXOJzQrjvO',
        'HOST': 'hopper.proxy.rlwy.net',
        'PORT': '26606',
    }
}
 """


# Base de datos principal
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv(
            'DATABASE_URL',
            'postgres://postgres:ERMDtLlspadbrHFCEySgYIaXOJzQrjvO@hopper.proxy.rlwy.net:26606/railway'
        )
    )
}

# Base de datos réplica
DATABASES['replica'] = dj_database_url.parse(
    os.getenv(
        'REPLICA_DATABASE_URL',
        'postgres://postgres:blCPlgNqEtUqPMEEKEsVEkPvNbXMtwOH@nozomi.proxy.rlwy.net:40484/railway'
    )
)

# base de datos replica 
# postgresql://postgres:blCPlgNqEtUqPMEEKEsVEkPvNbXMtwOH@nozomi.proxy.rlwy.net:40484/railway
# PGPASSWORD=blCPlgNqEtUqPMEEKEsVEkPvNbXMtwOH psql -h nozomi.proxy.rlwy.net -U postgres -p 40484 -d railway  
# railway connect Postgres

# base de datos replica render 
""" | Campo                 | Valor                                                   |
| --------------------- | ------------------------------------------------------- |
| **Destination name**  | `Postgres_Replica`                                      |
| **Host**              | `dpg-d170fop5pdvs73fr7ldg-a.oregon-postgres.render.com` |
| **Port**              | `5432`                                                  |
| **DB Name**           | `basereplica`                                           |
| **Default Schema**    | `public`                                                |
| **User**              | `basereplica_user`                                      |
| **Password**          | `IWvN1xty9pRdSEJ8ogokq5VOXAm7Krx1`                      |
| **SSL Mode**          | `require` (recomendado para conexiones externas)        |
| **SSH Tunnel Method** | `No Tunnel`                                             |
 """


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos multimedia
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary configuración
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME', 'dverop5st'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', '863615111676844'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', '3lbT8eRwP0sGi2DMhRCexFbyPtI'),
    'SECURE': True,
}

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="dverop5st",
    api_key="863615111676844",
    api_secret="3lbT8eRwP0sGi2DMhRCexFbyPtI"
)


# Django REST Framework + JWT

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# DRF Spectacular (documentación Swagger/OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'FreeMarket API',
    'DESCRIPTION': 'API para el sistema de ventas FreeMarket',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token JWT en el formato: Bearer <token>',
        }
    },
}

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://themause.netlify.app"
]
CSRF_TRUSTED_ORIGINS = [
    "https://themause.netlify.app",
]
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()

# Correo en desarrollo
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configuraciones de seguridad para producción
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Auto primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


