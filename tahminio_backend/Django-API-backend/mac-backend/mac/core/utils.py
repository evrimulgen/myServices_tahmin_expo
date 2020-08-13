import copy
from datetime import datetime, timedelta, time

from .constants import GROUPED_GAMES_LIST


def create_grouped_games(games):
    response = {}
    games_list = copy.deepcopy(GROUPED_GAMES_LIST)
    for game in games:
        if not games_list[game.string] in response:
            response[games_list[game.string]] = {}
        response[games_list[game.string]][game.string] = game.odd
        games_list.pop(game.string, None)
    for game in games_list:
        if games_list[game] not in response:
            response[games_list[game]] = {}
            response[games_list[game]][game] = '-'
        else:
            response[games_list[game]][game] = '-'
    return response


def calculate_minute(date):
    day_string = date.split(' ')[0].split('/')
    hour_string = date.split(' ')[1].split(':')

    day = int(day_string[0])
    month = int(day_string[1])
    year = int(day_string[2])

    hour = int(hour_string[0])
    minute = int(hour_string[1])

    now = datetime.today()
    before = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    minute = now - before

    return minute.seconds // 60
