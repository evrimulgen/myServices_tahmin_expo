from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .tasks import send_verification_email
from .utils import create_verification_key, twentyfour_hours


class User(AbstractUser):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.CharField(max_length=251, null=True, blank=True)
    email = models.EmailField(unique=True)
    profile_photo = models.ImageField(width_field="profile_photo_width", height_field="profile_photo_height", upload_to="users/images/%Y/%m/%d", null=True, blank=True)
    profile_photo_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    profile_photo_height = models.PositiveIntegerField(editable=False, null=True, blank=True)
    experience_point = models.PositiveIntegerField(default=0)
    skill_point = models.FloatField(default=0)
    remaining_modifier = models.PositiveIntegerField(default=5)
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = self.pk is None
        super(User, self).save(*args, **kwargs)
        if created:
            Token.objects.create(user=self)
            if not self.verified:
                verification_created = False
                while not verification_created:
                    try:
                        key = create_verification_key()
                        EmailVerification.objects.create(user=self, key=key)
                        verification_created = True
                        send_verification_email.delay(key, self.email)
                    except:
                        pass


class Followship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed_followships")
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'followed')


class EmailVerification(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    until = models.DateTimeField(default=twentyfour_hours)


class PasswordReset(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    until = models.DateTimeField(default=twentyfour_hours)


class MonthlyScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_point = models.FloatField(default=0)
    month = models.DateField()
