from datetime import datetime, timedelta, time

from django.core.management.base import BaseCommand

from mac.users.models import User
from mac.forum.models import Match, Game, Message, Prediction, Team, League


class Command(BaseCommand):
    """
    TODO: Add match events
    """
    help = "Mock database for testing"

    def handle(self, *args, **options):
        enis = User.objects.create(username='enis', email='enis@tahmin.io', password='#tahminio', verified=True, skill_point=101.4)
        deniz = User.objects.create(username='deniz', email='deniz@tahmin.io', password='#tahminio', verified=True, skill_point=-12.5)
        cucu = User.objects.create(username='cucu', email='cucu@tahmin.io', password='#tahminio', verified=True, skill_point=31.36)
        today = datetime.today()
        hour = time(12)
        home_team1 = Team.objects.create(name="Fenerbahce")
        away_team1 = Team.objects.create(name="Galatasaray")
        home_team2 = Team.objects.create(name="Liverpool")
        away_team2 = Team.objects.create(name="Manchester City")
        home_team3 = Team.objects.create(name="Real Madrid")
        away_team3 = Team.objects.create(name="Barcelona")
        turkish = League.objects.create(name="Turkish")
        spanish = League.objects.create(name="Spanish")
        english = League.objects.create(name="English")
        for x in range(100):
            # Matches for the next 100 days
            match1 = Match.objects.create(
                home_team=home_team1,
                away_team=away_team1,
                date=today + timedelta(days=x),
                time=hour,
                league=turkish
            )

            match2 = Match.objects.create(
                home_team=home_team3,
                away_team=away_team3,
                date=today + timedelta(days=x),
                time=hour,
                league=spanish
            )

            match3 = Match.objects.create(
                home_team=home_team2,
                away_team=away_team2,
                date=today + timedelta(days=x),
                time=hour,
                league=english,
                minute='31'
            )

            # Creating games for each, only MS games
            Game.objects.create(
                string='ms1',
                odd=1.55,
                match=match1,
            )
            Game.objects.create(
                string='msx',
                odd=3.2,
                match=match1,
            )
            Game.objects.create(
                string='ms2',
                odd=2.1,
                match=match1,
            )
            Game.objects.create(
                string='ms1',
                odd=1.55,
                match=match2,
            )
            Game.objects.create(
                string='msx',
                odd=3.2,
                match=match2,
            )
            Game.objects.create(
                string='ms2',
                odd=2.1,
                match=match2,
            )
            Game.objects.create(
                string='ms1',
                odd=1.55,
                match=match3,
            )
            Game.objects.create(
                string='msx',
                odd=3.2,
                match=match3,
            )
            Game.objects.create(
                string='ms2',
                odd=2.1,
                match=match3,
            )

            # Messages
            Message.objects.create(
                text='BALD FRAUD EXPOSED',
                user=enis,
                match=match3
            )
            Message.objects.create(
                text="City Liverpool'u ruyasinda bile yenemez",
                user=cucu,
                match=match3
            )
            Message.objects.create(
                text='gs ve fb bjkden korksun artik',
                user=deniz,
                match=match1
            )
            Message.objects.create(
                text='ruyamda gordum ms1',
                user=enis,
                match=match2
            )
            Message.objects.create(
                text='iyi bayramlar murat burul',
                user=cucu,
                match=match2
            )
            # Predictions
            Prediction.objects.create(
                text="Erzurum'dan gelen haci dedem fener siker dedi",
                game='ms1',
                user=enis,
                match=match1
            )
            Prediction.objects.create(
                text="Ozan Tufan oynuyor",
                game='msx',
                user=cucu,
                match=match1
            )
            Prediction.objects.create(
                text="turkiye ligi sikimde degil",
                game='ms2',
                user=deniz,
                match=match1
            )
            Prediction.objects.create(
                text="Klopp reis fraudiolayi expose eder",
                game='ms1',
                user=enis,
                match=match3
            )
            Prediction.objects.create(
                text="Ronalda hajum",
                game='ms1',
                user=deniz,
                match=match2
            )
            Prediction.objects.create(
                text="baba hissetti 0 gelir",
                game='msx',
                user=cucu,
                match=match2
            )
