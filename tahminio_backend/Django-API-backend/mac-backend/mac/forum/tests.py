import datetime

from django.test import TestCase
from rest_framework import status

from mac.core.tests import UserTestMixin
from mac.core.tasks import reward_punish_users
from mac.users.models import User
from .models import Match, Game, MatchEvent, Team, League


class ForumTestCase(TestCase, UserTestMixin):

    def test_get_matches(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        response = enis_client.get("/v1/matches/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = enis_client.get("/v1/matches/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_make_prediction(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

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

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'text': 'Fener tersten saplar',
            'game': 'h1'
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_prediction(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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
        prediction_id = response.data['id']

        response = enis_client.get('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = cucu_client.get('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_prediction(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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
        prediction_id = response.data['id']

        response = cucu_client.delete('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = enis_client.delete('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_prediction(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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
        prediction_id = response.data['id']

        data = {
            'game': 'msx'
        }
        response = cucu_client.patch('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = enis_client.patch('/v1/matches/%s/predictions/%s/' % (match.id, prediction_id), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_message(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
            time=datetime.time(12),
            league=league
        )

        data = {
            'text': 'gs ve fb bjkden korksun artik'
        }
        response = enis_client.post('/v1/matches/%s/messages/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_message(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
            time=datetime.time(12),
            league=league
        )

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
            time=datetime.time(12),
            league=league
        )

        data = {
            'text': 'gs ve fb bjkden korksun artik'
        }
        response = enis_client.post('/v1/matches/%s/messages/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message_id = response.data['id']

        data = {
            'text': 'Sari laciver sampiyon fener'
        }
        response = cucu_client.patch('/v1/matches/%s/messages/%s/' % (match.id, message_id), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = enis_client.patch('/v1/matches/%s/messages/%s/' % (match.id, message_id), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_message(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
            time=datetime.time(12),
            league=league
        )

        data = {
            'text': 'gs ve fb bjkden korksun artik'
        }
        response = enis_client.post('/v1/matches/%s/messages/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        message_id = response.data['id']

        response = cucu_client.delete('/v1/matches/%s/messages/%s/' % (match.id, message_id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = enis_client.delete('/v1/matches/%s/messages/%s/' % (match.id, message_id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_upvote_prediction(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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
        prediction_id = response.data['id']

        response = cucu_client.post("/v1/matches/%s/predictions/%s/upvote/" % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_undoupvote_prediction(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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
        prediction_id = response.data['id']

        response = cucu_client.post("/v1/matches/%s/predictions/%s/upvote/" % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = cucu_client.post("/v1/matches/%s/predictions/%s/undoupvote/" % (match.id, prediction_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_match(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        cucu.verified = True
        enis.save()
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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

        data = {
            'text': 'gs ve fb bjkden korksun artik'
        }
        response = enis_client.post('/v1/matches/%s/messages/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = cucu_client.post('/v1/matches/%s/messages/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = enis_client.get('/v1/matches/%s/' % match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_available_games(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
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

        response = enis_client.get('/v1/matches/%s/games/' % match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Maç Sonucu']['ms2'], 2.1)

    def test_get_match_events(self):
        enis, enis_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.date(2018, 4, 19),
            time=datetime.time(12),
            league=league
        )

        MatchEvent.objects.create(
            event_type='red_card',
            match=match,
            text='Volkan Demirel',
            time='85',
            side='home'
        )

        MatchEvent.objects.create(
            event_type='goal',
            match=match,
            text='Giuliano',
            time='45',
            side='home'
        )

        MatchEvent.objects.create(
            event_type='yellow_card',
            match=match,
            text='Selcuk Inan',
            time='54',
            side='away'
        )

        response = enis_client.get('/v1/matches/%s/events/' % match.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reward_and_punish_ms(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

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

        data = {
            'text': 'Fener tersten saplar',
            'game': 'msx',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, 15.5)
        self.assertEqual(deniz.skill_point, -0.32)

    def test_reward_punish_iyau15(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='iyau1,5-alt',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='iyau1,5-ust',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'iyau1,5-alt',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'iyau1,5-ust',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, 34.0)
        self.assertEqual(deniz.skill_point, -0.12)

    def test_reward_punish_au15(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='au1,5-alt',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='au1,5-ust',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'au1,5-alt',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'au1,5-ust',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)

    def test_reward_punish_au25(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='au2,5-alt',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='au2,5-ust',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'au2,5-alt',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'au2,5-ust',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)

    def test_reward_punish_au35(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        league = League.objects.create(name="Turkish")

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='au3,5-alt',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='au3,5-ust',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'au3,5-alt',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'au3,5-ust',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)

    def test_reward_punish_iy(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        cucu.verified = True
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='iy1',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='iyx',
            odd=4.5,
            match=match,
        )
        Game.objects.create(
            string='iy2',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'iy1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'iy2',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'iyx',
        }
        response = cucu_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)
        cucu = User.objects.get(id=cucu.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)
        self.assertEqual(cucu.skill_point, -0.45)

    def test_reward_punish_tc(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='tctek',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='tccift',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'tctek',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'tccift',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)

    def test_reward_punish_kg(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='kgvar',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='kgyok',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'kgvar',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'kgyok',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, 34.0)
        self.assertEqual(deniz.skill_point, -0.12)

    def test_reward_punish_tg(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='tg0-1',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='tg2-3',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 2
        match.away_team_score = 1
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'tg0-1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'tg2-3',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)

    def test_reward_punish_tg47(self):
        canberk, canberk_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        canberk.verified = True
        canberk.save()

        cucu.verified = True
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='tg4-6',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='tg7+',
            odd=1.2,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 3
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'tg7+',
        }
        response = canberk_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'tg4-6',
        }
        response = cucu_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        canberk = User.objects.get(id=canberk.id)
        cucu = User.objects.get(id=cucu.id)

        self.assertEqual(canberk.skill_point, -0.12)
        self.assertEqual(cucu.skill_point, 34.0)

    def test_reward_punish_handicap(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()

        deniz.verified = True
        deniz.save()

        cucu.verified = True
        cucu.save()

        home_team = Team.objects.create(name='Fenerbahce')
        away_team = Team.objects.create(name='Galatasaray')
        league = League.objects.create(name="Turkish")

        match = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.datetime.today(),
            time=datetime.time(12),
            league=league
        )

        Game.objects.create(
            string='h1',
            odd=3.4,
            match=match,
        )
        Game.objects.create(
            string='hx',
            odd=1.2,
            match=match,
        )
        Game.objects.create(
            string='h2',
            odd=1.5,
            match=match,
        )

        match.home_first_half_score = 0
        match.away_first_half_score = 1
        match.home_team_score = 3
        match.away_team_score = 2
        match.handicap = "-1"
        match.save()

        data = {
            'text': 'Fener tersten saplar',
            'game': 'h1',
        }
        response = enis_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'hx',
        }
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            'text': 'Fener tersten saplar',
            'game': 'h2',
        }
        response = cucu_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reward_punish_users(match)
        enis = User.objects.get(id=enis.id)
        deniz = User.objects.get(id=deniz.id)
        cucu = User.objects.get(id=cucu.id)

        self.assertEqual(enis.skill_point, -0.34)
        self.assertEqual(deniz.skill_point, 12.0)
        self.assertEqual(cucu.skill_point, -0.15)
