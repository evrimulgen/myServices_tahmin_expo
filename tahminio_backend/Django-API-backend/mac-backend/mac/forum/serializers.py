from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Match, Prediction, Game, Message, MatchEvent, Upvote, Team, League
from .constants import GAME_CHOICES
from mac.users.serializers import SimpleUserSerializer


class LeagueSerializer(serializers.ModelSerializer):

    class Meta:
        model = League
        fields = [
            "id",
            "name",
            "logo"
        ]


class TeamSerializer(serializers.ModelSerializer):
    logo = Base64ImageField()

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'logo'
        ]


class SimpleMatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer()
    away_team = TeamSerializer()
    league = LeagueSerializer()
    prediction_count = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'id',
            'home_team',
            'away_team',
            'score',
            'minute',
            'league',
            'datetime',
            'iddaa_code',
            'first_half_score',
            'handicap',
            'prediction_count',
            'message_count',
        ]

    def get_prediction_count(self, match):
        return Prediction.objects.filter(match=match).count()

    def get_message_count(self, match):
        return Message.objects.filter(match=match).count()


class PredictionSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    match = SimpleMatchSerializer(read_only=True)
    upvoted = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            'id',
            'game',
            'text',
            'user',
            'match',
            'upvote_count',
            'upvoted',
        ]

    def validate_game(self, value):
        if (value, value.upper()) in GAME_CHOICES:
            match = Match.objects.filter(id=self.context['pk'])
            if match.exists():
                match = match.first()
                games = Game.objects.filter(match=match, string=value)
                if games.exists():
                    return value
        raise serializers.ValidationError("Game is not allowed in this match")

    def get_upvoted(self, object):
        if self.context["request"].user.is_anonymous:
            return False
        return Upvote.objects.filter(prediction=object, upvoter=self.context["request"].user).exists()


class SimplePredictionSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    match = SimpleMatchSerializer(read_only=True)
    upvoted = serializers.SerializerMethodField()

    class Meta:
        model = Prediction
        fields = [
            'id',
            'match',
            'upvote_count',
            'game',
            'text',
            'user',
            'upvoted',
        ]

    def get_upvoted(self, object):
        if self.context["request"].user.is_anonymous:
            return False
        return Upvote.objects.filter(prediction=object, upvoter=self.context["request"].user).exists()


class MessageSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    match = SimpleMatchSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'text',
            'user',
            'match',
            'date_created',
        ]


class SimpleMessageSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    match = SimpleMatchSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'match',
            'text',
            'user',
            'date_created',
        ]


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = [
            'string',
            'odd'
        ]


class MatchEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchEvent
        fields = [
            'event_type',
            'text',
            'time',
        ]
