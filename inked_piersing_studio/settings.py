from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1o3z=oc$8&aa#d1w)#)pr)4fw#ds4ge)_jq(s@piqd3kq5pu1z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'products',
    'users',
    'blog',
    'orders',
    'cart',
    'appointments',
    'checkout',
    'coupons'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inked_piersing_studio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Исправлено
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Для MEDIA_URL и MEDIA_ROOT
            ],
        },
    },
]

WSGI_APPLICATION = 'inked_piersing_studio.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Статические файлы (CSS, JavaScript, images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Для production

# Медиа файлы (изображения товаров, и т.д.)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
CART_SESSION_ID = 'cart'

LOGIN_REDIRECT_URL = '/home'

# Email settings (добавьте или измените эти настройки)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Для реальной отправки
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Для отладки в консоли

EMAIL_HOST = 'smtp.gmail.com'  # Замените на ваш почтовый сервер
EMAIL_PORT = 587  # Замените на порт вашего почтового сервера (обычно 587 или 465)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  # Ваша почта.  Используем переменные окружения!
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  # Ваш пароль.  Используем переменные окружения!
EMAIL_USE_TLS = True  # Или EMAIL_USE_SSL = True, в зависимости от вашего почтового сервера
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL',
                                       'your_default_email@example.com')  # От кого будет отправляться письмо.  Используем переменные окружения!

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5" # ИСПРАВЛЕНО
CRISPY_TEMPLATE_PACK = "bootstrap5"  # ИСПРАВЛЕНО
# settings.py
"""
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Замените, если Redis работает на другом хосте/порту
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Опционально, если вам нужно хранить результаты задач
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'  # Или ваш часовой пояс
"""

load_dotenv()  # Загрузить переменные из .env

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

