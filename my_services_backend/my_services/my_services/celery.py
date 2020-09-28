import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_serices.settings.dev")

app = Celery("my_serices")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

