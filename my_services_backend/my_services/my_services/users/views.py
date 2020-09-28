from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth.models import User, Group
import datetime
from rest_framework import viewsets
from .serializers import SimpleUserSerializer

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

from .serializers import UserLoginSerializer, UserMeSerializer, UserDetailSerializer, ChangePasswordSerializer, \
    SimpleUserSerializer, ResetPasswordSerializer, ResetPasswordCreationSerializer
from .models import User, Followship, EmailVerification, PasswordReset
from .utils import get_random_string
from .tasks import send_passwordreset_email
from my_services.trophy.models import Trophy
from my_services.trophy.serializers import TrophySerializer
from .serializers import UserDetailSerializer
from rest_framework.permissions import IsAdminUser



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

    def post(self, request, *args, **kwargs):
        from rest_framework.authtoken.views import obtain_auth_token
        serializer = self.get_serializer(data=self.request.data)
        user = request.data
        import pdb;pdb.set_trace()
        serializer = serializer.create({
            'email': user['email'], 
            'password': user['password'], 
            'username': user['username']
            })
        serializer.is_valid(raise_exception=True)
        #user = serializer.create(user)
        return Response(UserMeSerializer(user).data)

# class UserSignupView(CreateAPIView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = UserMeSerializer

# class UserSignupView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = UserMeSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = UserMeSerializer(data=request.data)
#         data = {}
#         ac_id = len(User.objects.filter())
#         import pdb;pdb.set_trace() 
#         if serializer.is_valid():
#             #account = serializer.save()
#             data["id",] = account.id
#             data["username",] = account.username
#             data["email",] = account.email
#             data["token",] = account.token
#             data["password",] = account.password
#             data["profile_photo",] = account.profile_photo
#             data["bio",] = account.bio
#             data["first_name",] = account.first_name
#             data["last_name",] = account.last_name
#             data["remaining_modifier",] = account.remaining_modifier
#             data["verified",] = account.verified
#         else:
#             data = serializer.errors
#         user = serializer.create(self, account)
#         return Response(user)
#         #return Response(UserMeSerializer(user).data)


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

# class UserLoginView(GenericAPIView):
#     authentication_classes = []
#     permission_classes = []
#     serializer_class = UserLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         import pdb;pdb.set_trace()
#         return Response(UserMeSerializer(user).data)
#         #################################
#         #################################
#         #################################
#         #################################
#         #################################
#         #################################
#         #################################
#         import unicode
#         #import pdb;pdb.set_trace()
#         serializer = self.get_serializer(data=self.request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         content = {
#             'user': request.user,  # `django.contrib.auth.User` instance.
#             'auth': request.auth,  # None
#         }
#         return Response("content")


#@api_view(['GET'])    
@authentication_classes([])
@permission_classes([])
class HelloView(APIView):
    permission_classes = (IsAuthenticated,) 
    
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

@authentication_classes([])
@permission_classes([])
class UserViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]
    """
    API endpoint that allows users to be viewed or edited.
    """
    #serializer_class = SimpleUserSerializer
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        #import pdb;pdb.set_trace()
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = User.objects.all().order_by('-date_joined')
        #queryset = self.get_queryset()
        #serializer = UserSerializer(queryset, many=True)
        #return Response(serializer.data)
        # if token is not send, does not return
        content = {}
        for i in queryset:
            content[len(content)] = i.username
        print(content)
        return Response(content)
