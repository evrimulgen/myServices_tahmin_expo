import datetime

from django.test import TestCase
from rest_framework import status

from mac.core.tasks import reward_punish_users
from mac.users.tests import UserTestMixin
from mac.forum.models import Team, League, Game, Match
from .models import TrophyType, SuccessCount, Trophy


class TrophyTestCase(TestCase, UserTestMixin):

    def test_trophy_progression(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")
        TrophyType.objects.create(
            text="Turkiye Bronz",
            league=league,
            description="2 Turkiye tahmini",
            count=2,
        )

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='ms1',
            odd=1.55,
            match=match,
        )
        Game.objects.create(
            string='msx',
            odd=3.2,
            match=match,
        )
        Game.objects.create(
            string='ms2',
            odd=2.1,
            match=match,
        )

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        response = enis_client.get("/v1/users/me/trophies/")
        self.assertEqual(response.data, [])

        reward_punish_users(match)

        count = SuccessCount.objects.filter(user=enis)
        self.assertEqual(count.first().count, 1)

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='ms1',
            odd=1.55,
            match=match,
        )
        Game.objects.create(
            string='msx',
            odd=3.2,
            match=match,
        )
        Game.objects.create(
            string='ms2',
            odd=2.1,
            match=match,
        )

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        reward_punish_users(match)

        count = SuccessCount.objects.filter(user=enis)
        self.assertEqual(count.first().count, 2)

        trophy = Trophy.objects.filter(user=enis, league=league)
        self.assertTrue(trophy.exists())

    def test_get_trophy(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()

        enis.verified = True
        deniz.verified = True
        enis.save()
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")
        TrophyType.objects.create(
            text="Turkiye Bronz",
            league=league,
            description="2 Turkiye tahmini",
            count=2,
        )

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='ms1',
            odd=1.55,
            match=match,
        )
        Game.objects.create(
            string='msx',
            odd=3.2,
            match=match,
        )
        Game.objects.create(
            string='ms2',
            odd=2.1,
            match=match,
        )

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        response = enis_client.get("/v1/users/me/trophies/")
        self.assertEqual(response.data, [])

        reward_punish_users(match)

        count = SuccessCount.objects.filter(user=enis)
        self.assertEqual(count.first().count, 1)

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='ms1',
            odd=1.55,
            match=match,
        )
        Game.objects.create(
            string='msx',
            odd=3.2,
            match=match,
        )
        Game.objects.create(
            string='ms2',
            odd=2.1,
            match=match,
        )

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        reward_punish_users(match)

        count = SuccessCount.objects.filter(user=enis)
        self.assertEqual(count.first().count, 2)

        trophy = Trophy.objects.filter(user=enis, league=league)
        self.assertTrue(trophy.exists())

        response = enis_client.get("/v1/users/me/trophies/")
        self.assertEqual(response.data[0]["text"], "Turkiye Bronz")

        response = deniz_client.get("/v1/users/%s/trophies/" % enis.id)
        self.assertEqual(response.data[0]["text"], "Turkiye Bronz")
