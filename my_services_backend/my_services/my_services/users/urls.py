from django.urls import path, include
from django.contrib.auth.models import Group
from .models import User
from rest_framework import routers, serializers, viewsets
from . import views
from rest_framework.authtoken.views import obtain_auth_token  # Authantication for Token
from .views import UserLoginView, UserSignupView, UserDetailView, UserMeView, PasswordChangeView, UserFollowView, \
    UserUnfollowView, UsernameDetailView, VerifyUserView, UserSearchView, PasswordResetCreationView, PasswordResetView
    
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('users/login/', UserLoginView.as_view()),
    path('users/signup/', UserSignupView.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
    path('users/me/', UserMeView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/me/password/', PasswordChangeView.as_view()),
    path('users/<int:pk>/follow/', UserFollowView.as_view()),
    path('users/<int:pk>/unfollow/', UserUnfollowView.as_view()),
    path('users/activate/', VerifyUserView.as_view()),
    path('search/users/', UserSearchView.as_view()),
    path('users/forgot_password/', PasswordResetCreationView.as_view()),
    path('users/change_password/', PasswordResetView.as_view()),
    # This needs to be at the bottom, regex accepts everything
    path('users/<slug:username>/', UsernameDetailView.as_view()),
]
