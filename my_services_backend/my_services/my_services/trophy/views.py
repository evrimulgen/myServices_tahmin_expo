from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TrophySerializer
from .models import Trophy, TrophyType, SuccessCount


class TrophiesListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TrophySerializer

    def get_queryset(self):
        return Trophy.objects.filter(user=self.request.user)


class UserTrophiesListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TrophySerializer

    def get_queryset(self):
        return Trophy.objects.filter(user_id=self.kwargs["pk"])


class TrophyProgressionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        trophy_types = TrophyType.objects.filter()
        response = []
        for trophy in trophy_types:
            progression = SuccessCount.objects.filter(user=request.user, league=trophy.league)
            if progression.exists():
                finished = progression.first().count >= trophy.count
                response.append({
                    "text": trophy.text,
                    "description": trophy.description,
                    "finish_count": trophy.count,
                    "image": trophy.image if trophy.image else None,
                    "finished": finished,
                    "current_count": progression.first().count
                })
            else:
                response.append({
                    "text": trophy.text,
                    "description": trophy.description,
                    "finish_count": trophy.count,
                    "image": trophy.image if trophy.image else None,
                    "finished": False,
                    "current_count": 0
                })
        return Response(response, status=status.HTTP_200_OK)
