import os

from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1wc66*bnyv@tih@z#!4%x)l=#n1cu4*&1xzv)b1te25u=$a84s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['tahmin.io']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'storages',

    'mac.users',
    'mac.forum',
    'mac.core',
    'mac.trophy',
]

CELERY_BROKER_URL = 'amqp://admin:mypass@rabbit:5672'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Istanbul'
CELERY_BEAT_SCHEDULE = {
    "reset_modifier_counts": {
        "task": "mac.core.tasks.reset_modifier_counts",
        "schedule": crontab(day_of_week="0", hour="1"),
    },
    "get_iddaa_bulletin": {
        "task": "mac.core.tasks.get_iddaa_bulletin",
        "schedule": crontab(day_of_week="tue,fri", hour="1", minute="0")
    },
    "update_livescores": {
        "task": "mac.core.tasks.update_livescores",
        "schedule": crontab(),
    }
}

AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = 'eu-central-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'AKIAICCINCISO62ZL45A'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'tahminio'
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
)


ROOT_URLCONF = 'mac.urls'

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

WSGI_APPLICATION = 'mac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mac_db',
        'USER': 'mac_dbu',
        'PASSWORD': 'test',
        'HOST': 'mac_postgres',
        'PORT': '',
    }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'enisbt'
EMAIL_HOST_PASSWORD = '#tahminio2018'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AUTH_USER_MODEL = 'users.User'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
