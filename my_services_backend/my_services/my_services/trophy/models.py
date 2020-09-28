from django.db import models
from django.utils import timezone

from my_services.users.models import User


class Trophy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(width_field="image_width", height_field="image_height", upload_to="trophy/images", null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)


class SuccessCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


class TrophyType(models.Model):
    text = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    image = models.ImageField(width_field="image_width", height_field="image_height", upload_to="trophy/images", null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
