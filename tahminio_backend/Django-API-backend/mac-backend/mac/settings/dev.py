from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": None,
    }
}
