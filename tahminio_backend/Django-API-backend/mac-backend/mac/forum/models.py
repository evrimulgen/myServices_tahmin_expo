from datetime import datetime

from django.db import models
from django.utils import timezone

from mac.users.models import User
from .constants import GAME_CHOICES, MATCH_EVENT_CHOICES


class League(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(width_field="logo_width", height_field="logo_height", upload_to="leagues/logos", null=True, blank=True)
    logo_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    logo_height = models.PositiveIntegerField(editable=False, null=True, blank=True)


class Team(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(width_field="logo_width", height_field="logo_height", upload_to="teams/logos", null=True, blank=True)
    logo_width = models.PositiveIntegerField(editable=False, null=True, blank=True)
    logo_height = models.PositiveIntegerField(editable=False, null=True, blank=True)


class Match(models.Model):
    home_team = models.ForeignKey(Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_team', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    minute = models.CharField(max_length=10, null=True, blank=True)
    iddaa_code = models.CharField(max_length=10, null=True, blank=True)
    iddaa_id = models.IntegerField(null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    home_team_score = models.PositiveIntegerField(null=True, blank=True)
    away_team_score = models.PositiveIntegerField(null=True, blank=True)
    home_first_half_score = models.PositiveIntegerField(null=True, blank=True)
    away_first_half_score = models.PositiveIntegerField(null=True, blank=True)
    handicap = models.CharField(max_length=10, null=True, blank=True)
    done = models.BooleanField(default=False)

    @property
    def score(self):
        if self.home_team_score is None:
            return "-"
        else:
            return str(self.home_team_score) + " - " + str(self.away_team_score)

    @property
    def first_half_score(self):
        if self.home_first_half_score is None:
            return "-"
        else:
            return str(self.home_first_half_score) + " - " + str(self.away_first_half_score)

    @property
    def datetime(self):
        date = datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute)
        return date.timestamp()


class MatchEvent(models.Model):
    event_type = models.CharField(max_length=100, choices=MATCH_EVENT_CHOICES)
    time = models.CharField(max_length=20)
    side = models.CharField(max_length=10, choices=[('home', 'Home'), ('away', "Away")])
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)


class Message(models.Model):
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


class Game(models.Model):
    string = models.CharField(max_length=20, choices=GAME_CHOICES)
    odd = models.FloatField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE)


class Prediction(models.Model):
    text = models.TextField(max_length=500, null=True, blank=True)
    game = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)

    @property
    def upvote_count(self):
        return Upvote.objects.filter(prediction=self).count()

    class Meta:
        unique_together = ('match', 'user')


class Upvote(models.Model):
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    upvoter = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("prediction", "upvoter")
