from .base import *

ALLOWED_HOSTS = ['138.68.73.29', 'api.tahmin.io']

DEBUG=True

CELERY_BROKER_URL = 'amqp://test:test@localhost:5672'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tahmin_db',
        'USER': 'tahmin_dbu',
        'PASSWORD': 'tahmin_test',
        'HOST': '',
        'PORT': '5432',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": None,
    }
}
