from django.test import TestCase
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient

from mac.users.models import User


class UserTestMixin(object):
    def create_user_and_user_client(self):
        user = User.objects.create_user(
            username=get_random_string(6),
            password=get_random_string(9),
            email=get_random_string(5) + '@bobmail.com',
            first_name=get_random_string(5),
            last_name=get_random_string(5),
        )
        client = APIClient()
        client.default_format = 'json'
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.auth_token.key)
        return user, client
