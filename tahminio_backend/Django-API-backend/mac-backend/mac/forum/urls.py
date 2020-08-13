from django.urls import path

from .views import MatchView, PredictionView, PredictionDetailView, MessageView, MessageDetailView, UpvoteView, \
    UnUpvoteView, MatchDetailView, AvailableGamesView, MatchEventsView, MatchlistMeta

urlpatterns = [
    path('matches/', MatchView.as_view()),
    path('matches/<int:pk>/predictions/', PredictionView.as_view()),
    path('matches/<int:match_pk>/predictions/<int:pk>/', PredictionDetailView.as_view()),
    path('matches/<int:match_pk>/predictions/<int:pk>/upvote/', UpvoteView.as_view()),
    path('matches/<int:match_pk>/predictions/<int:pk>/undoupvote/', UnUpvoteView.as_view()),
    path('matches/<int:pk>/messages/', MessageView.as_view()),
    path('matches/<int:match_pk>/messages/<int:pk>/', MessageDetailView.as_view()),
    path('matches/<int:pk>/', MatchDetailView.as_view()),
    path('matches/<int:match_pk>/games/', AvailableGamesView.as_view()),
    path('matches/<int:match_pk>/events/', MatchEventsView.as_view()),
    path('matches/meta/', MatchlistMeta.as_view()),
]
