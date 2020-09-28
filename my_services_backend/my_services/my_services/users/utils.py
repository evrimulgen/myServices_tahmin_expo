from datetime import timedelta

from django.utils import timezone
from django.utils.crypto import get_random_string


def twentyfour_hours():
    return timezone.now() + timedelta(hours=24)


def six_hours():
    return timezone.now() + timedelta(hours=6)


def create_verification_key():
    return get_random_string(50)
