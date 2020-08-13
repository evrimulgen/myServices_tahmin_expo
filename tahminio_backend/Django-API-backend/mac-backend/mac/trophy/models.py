from django.db import models
from django.utils import timezone

from mac.users.models import User
from mac.forum.models import League


class Trophy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255, null=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(width_field="image_width", height_field="image_height", upload_to="trophy/images", null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)


class SuccessCount(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)


class TrophyType(models.Model):
    text = models.CharField(max_length=255)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    count = models.PositiveIntegerField()
    image = models.ImageField(width_field="image_width", height_field="image_height", upload_to="trophy/images", null=True, blank=True)
    image_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    image_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
