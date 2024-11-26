import os
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from django.core.mail.backends import smtp

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-r9@wm9hhnl0j_j&&o9=*o@&ot(55ge74%zzrr!&_(&xwillywq'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework_simplejwt',
    'django_filters',
    'materials',
    'users',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

# settings.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # Замените на адрес вашего фронтенда
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",  # Замените на адрес вашего фронтенда
]

CORS_ALLOW_ALL_ORIGINS = False

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'm7',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY', 'sk_test_51QPDKfJDSkFqqzU94ZvxXMNqPPSCYvqifL4PmmiAM08Lw4gg4Y9sHYov7LLSpQ5OXv0mnXB4PCxiNyIMqrTXrc8u00opKzGGYt')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY', 'pk_test_51QPDKfJDSkFqqzU9CsSs1NAlyEfmAp0NIv7Brb7ewJbZunJSyIqIXAPT13xHOb26px988HcdsRETeerSvbqVeTm100JtTgv93F')

CELERY_BROKER_URL = 'redis://localhost:6379' # Например, Redis, который по умолчанию работает на порту 6379

# URL-адрес брокера результатов, также Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Часовой пояс для работы Celery
CELERY_TIMEZONE = "Australia/Tasmania"

# Флаг отслеживания выполнения задач
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULE = {
    'block-inactive-users-every-day': {
        'task': 'materials.tasks.block_inactive_users',
        'schedule': crontab(hour=0, minute=0),
    },
}

EMAIL_HOST: 'smtp.yandex.ru'
EMAIL_PORT: 465
EMAIL_HOST_USER: 'koteika.koteevitch@yandex.ru'
EMAIL_HOST_PASSWORD: 'yhmqejdprtxdiiyp'
EMAIL_USE_TLS: False
EMAIL_USE_SSL: True
