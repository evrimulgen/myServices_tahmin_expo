from django.core.management.base import BaseCommand
from leaderboard.leaderboard import Leaderboard

from mac.users.models import User, MonthlyScore


class Command(BaseCommand):
    help = "Populate leaderboard"

    def handle(self, *args, **options):
        # All time leaderboard
        highscores = Leaderboard('highscores')
        users = User.objects.filter()
        for user in users:
            highscores.rank_member(user.id, user.skill_point)

        # Monthly leaderboards
        monthly_scores = MonthlyScore.objects.filter()
        for monthly in monthly_scores:
            monthly_highscores = Leaderboard(str(monthly.month.month) + '-' + str(monthly.month.year) + '_highscores', host="redis")
            monthly_highscores.rank_member(monthly.user.id, monthly.skill_point)
