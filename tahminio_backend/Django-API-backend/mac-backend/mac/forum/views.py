import datetime

from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import caches

from .permissions import IsVerified
from .models import Match, Prediction, Message, Upvote, Game, MatchEvent
from .serializers import SimpleMatchSerializer, PredictionSerializer, MessageSerializer, SimplePredictionSerializer, \
    SimpleMessageSerializer, GameSerializer, MatchEventSerializer
from mac.core.utils import create_grouped_games


class MatchView(ListAPIView):
    serializer_class = SimpleMatchSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.GET.get("date") is None:
            return Match.objects.filter(date=datetime.date.today()).order_by('time')
        else:
            dates = self.request.GET.get("date").split("-")
            date = datetime.date(int(dates[2]), int(dates[1]), int(dates[0]))
            return Match.objects.filter(date=date).order_by('time')

    @method_decorator(cache_page(5))
    def dispatch(self, *args, **kwargs):
        return super(MatchView, self).dispatch(*args, **kwargs)


class PredictionView(ListCreateAPIView):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.filter(match=self.kwargs["pk"])

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return [IsAuthenticated(), IsVerified()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, match=Match.objects.get(id=self.kwargs['pk']))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk'] = self.kwargs['pk']
        return context

    def post(self, request, *args, **kwargs):
        prediction = Prediction.objects.filter(match=self.kwargs['pk'], user=request.user)
        if prediction.exists():
            raise ValidationError("You can't make more than one prediction for a match")
        response = super().post(request, *args, **kwargs)
        return response


class PredictionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PredictionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return [IsAuthenticated(), IsVerified()]

    def get_queryset(self):
        if self.request.method == 'GET':
            prediction = Prediction.objects.filter(id=self.kwargs['pk'])
            return prediction
        else:
            prediction = Prediction.objects.filter(id=self.kwargs['pk'], user=self.request.user)
            if prediction.exists():
                return prediction
            else:
                raise PermissionDenied

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk'] = self.kwargs['match_pk']
        return context


class MessageView(ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return [IsAuthenticated(), IsVerified()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, match=Match.objects.get(id=self.kwargs['pk']))


class MessageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return AllowAny(),
        else:
            return IsAuthenticated(),

    def get_queryset(self):
        if self.request.method == 'GET':
            prediction = Message.objects.filter(id=self.kwargs['pk'])
            return prediction
        else:
            prediction = Message.objects.filter(id=self.kwargs['pk'], user=self.request.user)
            if prediction.exists():
                return prediction
            else:
                raise PermissionDenied


class UpvoteView(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request, *args, **kwargs):
        Upvote.objects.create(prediction_id=self.kwargs["pk"], upvoter=request.user)
        return Response({'status': 'OK'})


class UnUpvoteView(APIView):
    permission_classes = [IsAuthenticated, IsVerified]

    def post(self, request, *args, **kwargs):
        Upvote.objects.filter(prediction_id=self.kwargs["pk"], upvoter=request.user).delete()
        return Response({'status': 'OK'})


class MatchDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        cache_control = caches["default"].get(self.kwargs["pk"])
        if cache_control is not None:
            return Response(data=cache_control, status=status.HTTP_200_OK)
        response = {}
        match = Match.objects.get(id=self.kwargs["pk"])
        match_json = SimpleMatchSerializer(instance=match)
        predictions = Prediction.objects.filter(match=match).order_by('-id')[:5]
        predictions = SimplePredictionSerializer(data=predictions, many=True, context={"request": request})
        messages = Message.objects.filter(match=match).order_by('-id')[:5]
        messages = SimpleMessageSerializer(data=messages, many=True)
        games = Game.objects.filter(match=match)
        games = create_grouped_games(games)
        home_events = MatchEvent.objects.filter(match=match, side='home')
        away_events = MatchEvent.objects.filter(match=match, side='away')
        home_events = MatchEventSerializer(data=home_events, many=True)
        away_events = MatchEventSerializer(data=away_events, many=True)
        home_events.is_valid()
        away_events.is_valid()
        messages.is_valid()
        predictions.is_valid()
        response['events'] = {}
        response['events']['home_events'] = home_events.data
        response['events']['away_events'] = away_events.data
        response["messages"] = messages.data
        response["predictions"] = predictions.data
        response["match"] = match_json.data
        response['games'] = games
        caches["default"].set(self.kwargs["pk"], response, 10)
        return Response(data=response, status=status.HTTP_200_OK)


class AvailableGamesView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer

    def get(self, request, *args, **kwargs):
        return Response(data=create_grouped_games(Game.objects.filter(match_id=self.kwargs['match_pk'])), status=status.HTTP_200_OK)


class MatchEventsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = MatchEventSerializer

    def get(self, request, *args, **kwargs):
        response = {}
        home_events = MatchEvent.objects.filter(match_id=self.kwargs['match_pk'], side='home')
        away_events = MatchEvent.objects.filter(match_id=self.kwargs['match_pk'], side='away')
        home_events = MatchEventSerializer(data=home_events, many=True)
        away_events = MatchEventSerializer(data=away_events, many=True)
        home_events.is_valid()
        away_events.is_valid()
        response['home_events'] = home_events.data
        response['away_events'] = away_events.data
        return Response(data=response, status=status.HTTP_200_OK)


class MatchlistMeta(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        response = {}
        response['dates'] = caches['default'].get('dates')
        return Response(data=response, status=status.HTTP_200_OK)
