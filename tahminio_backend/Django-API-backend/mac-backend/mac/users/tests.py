import datetime
from datetime import timedelta

from django.test import TestCase
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import User, Followship, EmailVerification, PasswordReset
from mac.forum.models import Game, Team, League, Match


class UserTestMixin(object):

    def create_user_and_user_client(self):
        user = User.objects.create_user(
            username=get_random_string(6),
            password="#tahminio",
            email=get_random_string(5) + '@bobmail.com',
            first_name=get_random_string(5),
            last_name=get_random_string(5),
            bio="Best backend developer of the world",
            verified=True,
        )
        client = APIClient()
        client.default_format = 'json'
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        return user, client

    def create_mock_user_data(self):
        data = {
            'username': get_random_string(6),
            'password': get_random_string(8),
            'email': get_random_string(5) + '@bobmail.com',
            'first_name': get_random_string(5),
            'last_name': get_random_string(5),
            'bio': "Best backend developer of the world",
        }
        return data


class UserTestCase(TestCase, UserTestMixin):

    def test_token_creation(self):
        data = {
            'username': 'enisbt',
            'password': 'this_is_a_password1',
            'email': 'enisbehict@yandex.com.tr',
            'first_name': 'Enis Behic',
            'last_name': 'Tuysuz',
        }
        user = User.objects.create(**data)
        token, created = Token.objects.get_or_create(user=user)
        self.assertFalse(created)

    def test_user_signup(self):
        user_client = APIClient()
        user_client.default_format = 'json'
        data = self.create_mock_user_data()

        response = user_client.post('/v1/users/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {
            'username': 'enisbt',
            'password': 'this_is_a_password1',
            'email': 'enisbehict@yandex.com.tr',
            'first_name': 'Enis Behic',
            'last_name': 'Tuysuz',
        }
        User.objects.create_user(**data)
        user_client = APIClient()
        user_client.default_format = 'json'

        data = {
            'username': 'enisbt',
            'password': 'this_is_a_password1'
        }
        response = user_client.post('/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_me_get(self):
        user, user_client = self.create_user_and_user_client()
        response = user_client.get('/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_patch(self):
        user, user_client = self.create_user_and_user_client()
        response = user_client.get('/v1/users/me/')
        pre_patch_first_name = response.data['first_name']
        data = {
            'first_name': 'Enis Behic'
        }
        response = user_client.patch('/v1/users/me/', data=data)
        self.assertFalse(pre_patch_first_name == response.data['first_name'])
        self.assertEqual(response.data['first_name'], 'Enis Behic')

    def test_user_profile_delete(self):
        user, user_client = self.create_user_and_user_client()
        response = user_client.get('/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_client.delete('/v1/users/me/')
        response = user_client.get('/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        response = cucu_client.get("/v1/users/%s/" % enis.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse("token" in response.data)

    def test_change_user_password(self):
        enis, enis_client = self.create_user_and_user_client()

        data = {
            'old_password': '#tahminio',
            'new_password': '#tahminio1'
        }
        response = enis_client.patch('/v1/users/me/password/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'username': enis.username,
            'password': "#tahminio1"
        }
        response = enis_client.post('/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_user(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        self.assertFalse(Followship.objects.filter(followed=cucu).exists())

        response = enis_client.post("/v1/users/%s/follow/" % cucu.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(Followship.objects.filter(followed=cucu).exists())

        response = enis_client.post("/v1/users/%s/follow/" % enis.id)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        self.assertFalse(Followship.objects.filter(followed=cucu).exists())

        response = enis_client.post("/v1/users/%s/follow/" % cucu.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Followship.objects.filter(followed=cucu).exists())

        response = enis_client.post("/v1/users/%s/unfollow/" % cucu.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Followship.objects.filter(followed=cucu).exists())

    def test_get_user_with_username(self):
        enis, enis_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        response = cucu_client.get('/v1/users/%s/' % enis.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], enis.username)

    def test_get_user_verification(self):
        enis_client = APIClient()
        enis_client.default_format = 'json'
        data = self.create_mock_user_data()

        response = enis_client.post('/v1/users/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        enis_id = response.data['id']

        verification = EmailVerification.objects.filter(user_id=enis_id)
        self.assertTrue(verification.exists())

        response = enis_client.get('/v1/users/activate/?key=%s' % verification.first().key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(id=enis_id)
        self.assertTrue(user.verified)

    def test_search_user(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()

        response = deniz_client.get('/v1/search/users/?query=' + enis.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["username"], enis.username)

    def test_create_password_reset(self):
        enis, enis_client = self.create_user_and_user_client()

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.username
        }
        response = enis_client.post("/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertTrue(password_reset.exists())
        password_reset.delete()

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.email
        }
        response = enis_client.post("/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        enis = User.objects.create_user(
            username="enis",
            password="#tahminio",
            email=get_random_string(5) + '@bobmail.com',
            first_name=get_random_string(5),
            last_name=get_random_string(5),
            bio="Best backend developer of the world",
            verified=True,
        )
        enis_client = APIClient()
        enis_client.default_format = 'json'
        enis_client.credentials(HTTP_AUTHORIZATION='Token ' + enis.auth_token.key)

        data = {
            'username': 'enis',
            'password': '#tahminio'
        }
        response = enis_client.post('/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertFalse(password_reset.exists())

        data = {
            "user_identifier": enis.username
        }
        response = enis_client.post("/v1/users/forgot_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        password_reset = PasswordReset.objects.filter(user=enis)
        self.assertTrue(password_reset.exists())

        password_reset = password_reset.first()

        data = {
            "key": password_reset.key,
            "password": "1"
        }
        response = enis_client.post("/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        password_reset.until = timezone.now() - timedelta(hours=2)
        password_reset.save()

        data = {
            "key": password_reset.key,
            "password": "#tahminio_is_awesome"
        }
        response = enis_client.post("/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        password_reset.until = timezone.now() + timedelta(hours=24)
        password_reset.save()

        data = {
            "key": password_reset.key,
            "password": "#tahminio_is_awesome"
        }
        response = enis_client.post("/v1/users/change_password/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {
            'username': 'enis',
            'password': '#tahminio_is_awesome'
        }
        response = enis_client.post('/v1/users/login/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_username_blacklist(self):
        user_client = APIClient()
        user_client.default_format = 'json'
        data = {
            "username": ".well-known",
            "password": "#tahminio",
            'email': get_random_string(5) + '@bobmail.com',
            'first_name': get_random_string(5),
            'last_name': get_random_string(5),
            'bio': "Best backend developer of the world",
        }

        response = user_client.post('/v1/users/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_feed(self):
        enis, enis_client = self.create_user_and_user_client()
        deniz, deniz_client = self.create_user_and_user_client()
        cucu, cucu_client = self.create_user_and_user_client()

        enis.verified = True
        enis.save()
        deniz.verified = True
        deniz.save()
        cucu.verified = True
        cucu.save()

        response = enis_client.get('/v1/users/feed/')
        self.assertEqual(response.data, [])

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
        response = deniz_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = enis_client.get('/v1/users/feed/')
        self.assertEqual(response.data, [])

        response = enis_client.post("/v1/users/%s/follow/" % deniz.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = enis_client.get('/v1/users/feed/')
        self.assertEqual(len(response.data), 1)

        data = {
            'text': 'Fener tersten saplar',
            'game': 'ms1',
        }
        response = cucu_client.post('/v1/matches/%s/predictions/' % match.id, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = enis_client.get('/v1/users/feed/')
        self.assertEqual(len(response.data), 1)

        response = enis_client.post("/v1/users/%s/follow/" % cucu.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = enis_client.get('/v1/users/feed/')
        self.assertEqual(len(response.data), 2)
