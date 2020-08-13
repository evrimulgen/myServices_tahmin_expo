import datetime

from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, \
    UpdateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import password_validation
from django.core import exceptions
from leaderboard.leaderboard import Leaderboard

from .serializers import UserLoginSerializer, UserMeSerializer, UserDetailSerializer, ChangePasswordSerializer, \
    SimpleUserSerializer, ResetPasswordSerializer, ResetPasswordCreationSerializer
from .models import User, Followship, EmailVerification, PasswordReset
from .utils import get_random_string
from .tasks import send_passwordreset_email
from mac.trophy.models import Trophy
from mac.trophy.serializers import TrophySerializer
from mac.forum.serializers import PredictionSerializer
from mac.forum.models import Prediction


class UserLoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(UserMeSerializer(user).data)


class UserSignupView(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UserMeSerializer


class UserMeView(RetrieveUpdateDestroyAPIView):
    permission__classes = [IsAuthenticated]
    serializer_class = UserMeSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object

    def get(self, request, *args, **kwargs):
        response = super(UserMeView, self).get(request, *args, **kwargs)
        trophies = Trophy.objects.filter(user=self.request.user)
        trophies = TrophySerializer(trophies, many=True)
        response.data["trophies"] = trophies.data
        return response


class UsernameDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])

    def get_object(self):
        return User.objects.get(username=self.kwargs['username'])


class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        response = super(UserDetailView, self).get(request, *args, **kwargs)
        trophies = Trophy.objects.filter(user_id=self.kwargs["pk"])
        trophies = TrophySerializer(trophies, many=True)
        response.data["trophies"] = trophies.data
        return response


class PasswordChangeView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        object = self.request.user
        self.check_object_permissions(self.request, object)
        return object

    def update(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            object.set_password(serializer.data.get("new_password"))
            object.save()
            return Response(UserMeSerializer(object).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollowView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs["pk"])

    # TODO: Improve error handling
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id == self.request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Followship.objects.get_or_create(follower=self.request.user, followed=user)
        return Response({"status": "OK"})


class UserUnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Followship.objects.filter(follower=self.request.user, followed_id=self.kwargs["pk"]).delete()
        return Response({"status": "OK"})


class VerifyUserView(APIView):

    def get_permissions(self):
        return AllowAny(),

    def get(self, request, *args, **kwargs):
        verification = EmailVerification.objects.filter(key=request.GET.get('key'))
        if verification.exists():
            verification = verification.first()
            if verification.until > timezone.now():
                verification.user.verified = True
                verification.user.save()
                return Response({"status": "OK"})
            raise ValidationError('Not verified in time')
        raise ValidationError('Verification not found')


class UserSearchView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        return User.objects.filter(username__icontains=self.request.GET.get('query'))


class PasswordResetCreationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordCreationSerializer(data=request.data)
        if serializer.is_valid():
            sender = None
            user = User.objects.filter(username=serializer.data["user_identifier"])
            if user.exists():
                sender = user.first()
            user = User.objects.filter(email=serializer.data["user_identifier"])
            if user.exists():
                sender = user.first()
            if sender:
                key = get_random_string(50)
                while PasswordReset.objects.filter(key=key):
                    key = get_random_string(50)
                PasswordReset.objects.create(user=sender, key=key)
                send_passwordreset_email.delay(key, sender.email)
            else:
                pass
            return Response(status=status.HTTP_200_OK)
        return Response([{"user_identifier": "This field is required"}], status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password_reset = PasswordReset.objects.filter(key=serializer.data["key"])
            if password_reset.exists():
                # Checking if the key is valid
                until = password_reset.first().until
                if timezone.now() > until:
                    return Response([{"key": "The key is expired"}], status=status.HTTP_400_BAD_REQUEST)
                user = password_reset.first().user
                # Password validation
                try:
                    password_validation.validate_password(serializer.data["password"])
                except exceptions.ValidationError:
                    return Response([{"password": "Invalid password"}], status=status.HTTP_400_BAD_REQUEST)
                user.set_password(serializer.data["password"])
                user.save()
                password_reset.delete()
                return Response({"Password changed successfully"}, status=status.HTTP_200_OK)
            else:
                return Response([{"key": "The key doesn't exists"}], status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AllLeaderboardView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SimpleUserSerializer

    def get_queryset(self):
        highscores = Leaderboard('highscores')
        page = int(self.kwargs["page"])
        users = highscores.leaders(page)
        user_ids = []
        for user in users:
            user_ids.append(user["member"])
        return User.objects.filter(id__in=user_ids).order_by("-skill_point")


class MonthlyLeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        if request.GET.get("month") is None:
            today = datetime.datetime.today()
            month = str(today.month) + "-" + str(today.year)
        else:
            month = request.GET.get("month")
        monthly_highscores = Leaderboard(month + "_highscores", host="redis")
        page = int(self.kwargs["page"])
        users = monthly_highscores.leaders(page)
        response = []
        for user_id in users:
            user = User.objects.get(id=user_id["member"])
            response.append({
                "id": user.id,
                "username": user.username,
                "skill_point": user_id["score"],
                "profile_photo": user.profile_photo if user.profile_photo else None
            })
        return Response(response, status=status.HTTP_200_OK)


class AllTimeLeaderboardTotalPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        highscores = Leaderboard('highscores')
        return Response({"total_pages": highscores.total_pages()})


class FeedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PredictionSerializer

    def get_queryset(self):
        user_ids = list(Followship.objects.filter(follower=self.request.user).values_list('followed', flat=True))
        return Prediction.objects.filter(user_id__in=user_ids)
