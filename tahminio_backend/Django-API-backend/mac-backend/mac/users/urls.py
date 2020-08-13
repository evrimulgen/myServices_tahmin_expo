from django.urls import path

from mac.trophy.views import TrophiesListView, UserTrophiesListView, TrophyProgressionView
from .views import UserLoginView, UserSignupView, UserDetailView, UserMeView, PasswordChangeView, UserFollowView, \
    UserUnfollowView, UsernameDetailView, VerifyUserView, UserSearchView, PasswordResetCreationView, PasswordResetView, \
    AllLeaderboardView, MonthlyLeaderboardView, AllTimeLeaderboardTotalPageView, FeedView

urlpatterns = [
    path('users/login/', UserLoginView.as_view()),
    path('users/signup/', UserSignupView.as_view()),
    path('users/me/', UserMeView.as_view()),
    path('users/me/trophies/', TrophiesListView.as_view()),
    path('users/me/progression/', TrophyProgressionView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<int:pk>/trophies/', UserTrophiesListView.as_view()),
    path('users/me/password/', PasswordChangeView.as_view()),
    path('users/<int:pk>/follow/', UserFollowView.as_view()),
    path('users/<int:pk>/unfollow/', UserUnfollowView.as_view()),
    path('users/activate/', VerifyUserView.as_view()),
    path('search/users/', UserSearchView.as_view()),
    path('users/forgot_password/', PasswordResetCreationView.as_view()),
    path('users/change_password/', PasswordResetView.as_view()),
    path('leaders/<int:page>/', AllLeaderboardView.as_view()),
    path('leaders/total_pages/', AllTimeLeaderboardTotalPageView.as_view()),
    path('leaders/monthly/<int:page>/', MonthlyLeaderboardView.as_view()),
    path('users/feed/', FeedView.as_view()),
    # This needs to be at the bottom, regex accepts everything
    path('users/<slug:username>/', UsernameDetailView.as_view()),
]
