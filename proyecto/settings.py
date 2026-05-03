# CONFIGURACIÓN DEL SISTEMA - UNIE
# Este archivo contiene todos los ajustes importantes de la web (Base de datos, Apps, etc.)

import os
from pathlib import Path

# Buscamos la carpeta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ¡¡OJO!! Esto debería ser secreto si estuviéramos en producción real
SECRET_KEY = 'django-insecure-unifix-super-secret-key'

# En desarrollo lo dejamos en True para ver los errores
DEBUG = True

ALLOWED_HOSTS = ['*']

# Mis aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías externas que nos sirven para el estilo y la API
    'rest_framework',
    'corsheaders',
    
    # Mi aplicación de gestión de campus
    'gestion',
]

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

ROOT_URLCONF = 'proyecto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Aquí le decimos dónde están las carpetas con el diseño HTML
        'DIRS': [os.path.join(BASE_DIR, 'gestion', 'templates')],
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

WSGI_APPLICATION = 'proyecto.wsgi.application'

# Usamos SQLite que es un archivo sencillo para no complicarnos con servidores SQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Modelo de usuario personalizado con Roles
AUTH_USER_MODEL = 'gestion.User'

# Validaciones de contraseña (las que vienen por defecto con Django)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Rutas para el acceso de usuarios
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Idioma y Hora (Puesto para España)
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, Imágenes)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True
