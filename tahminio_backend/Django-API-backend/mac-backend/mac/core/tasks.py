import json
from datetime import datetime

from celery import task
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from leaderboard.leaderboard import Leaderboard

from mac.trophy.models import Trophy, TrophyType, SuccessCount
from mac.forum.models import Team, Match, Game, Prediction, League
from mac.forum.serializers import SimpleMatchSerializer
from mac.users.models import User, MonthlyScore
from .constants import GAMES, GAMES_LIST
from .utils import calculate_minute


@task()
def reset_modifier_counts():
    User = get_user_model()
    User.objects.filter().update(remaining_modifier=5)


@task()
def get_iddaa_bulletin():
    r = requests.get('https://bulletin.iddaa.com/data/bulletin-with-percentage')
    odds_json = json.loads(r.text)
    matches = odds_json['data']['bulletin']['football']['eventList']
    IMAGE_URL = "https://cdn.broadage.com/images-teams/soccer/82x82/"

    for match in matches:
        home_team, home_created = Team.objects.get_or_create(name=match["homeTeam"])
        if home_created:
            url = IMAGE_URL + str(match["helperInfo"]["homeTeam"]["id"]) + ".png"
            request = requests.get(url, stream=True)
            file_name = url.split('/')[-1]
            lf = NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                lf.write(block)
            home_team.logo.save(file_name, File(lf))
        away_team, away_created = Team.objects.get_or_create(name=match["awayTeam"])
        if away_created:
            url = IMAGE_URL + str(match["helperInfo"]["awayTeam"]["id"]) + ".png"
            request = requests.get(url, stream=True)
            file_name = url.split('/')[-1]
            lf = NamedTemporaryFile()
            for block in request.iter_content(1024 * 8):
                if not block:
                    break
                lf.write(block)
            away_team.logo.save(file_name, File(lf))
        if Match.objects.filter(iddaa_id=match["matchId"]).exists():
            continue
        league, league_created = League.objects.get_or_create(name=match["helperInfo"]["tournament"]["name"])
        match_object = Match.objects.create(
            home_team=home_team,
            away_team=away_team,
            date=datetime.strptime(match["eventDate"], "%d.%m.%Y").date(),
            time=datetime.strptime(match["eventHour"], "%H:%M:%S").time(),
            iddaa_code=str(match["matchCode"]),
            iddaa_id=match["id"],
            league=league,
        )
        for odd in match['oddList']:
            if odd['type'] in GAMES:
                Game.objects.create(match=match_object, string=GAMES[odd["type"]], odd=float(odd["v"]))


@task()
def update_livescores():
    url = "https://brdg-4adf3615-2821-474a-96b8-b7bbdd73fa40.azureedge.net/livescore/matchlist"

    payload = "{\"coverageId\":\"EA5BC554-267B-42A0-8EDD-E8ECC2766529\",\"options\":{\"lang\":\"tr-TR\",\"grouping\":\"date\",\"betCode\":true,\"sportId\":1,\"origin\":\"iddaa.com\",\"forceFullData\":true,\"timeZone\":3}}"
    headers = {
        'referer': "https://www.iddaa.com/futbol-canli-skor/",
        'origin': "https://www.iddaa.com",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'postman-token': "1d1d43f7-e091-b779-c73d-c48e7d8f2151"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    stages = json.loads(response.text)['initialData']

    for stage in stages:
        matches = stage['matches']
        for match in matches:
            home_team_object = Team.objects.filter(name=match['homeTeam']['middleName'])
            away_team_object = Team.objects.filter(name=match['awayTeam']['middleName'])
            if home_team_object.exists() and away_team_object.exists():
                home_team_object = home_team_object.first()
                away_team_object = away_team_object.first()
            else:
                continue
            match_object = Match.objects.filter(home_team=home_team_object, away_team=away_team_object, done=False)
            if match_object.exists():
                match_object = match_object.first()
            else:
                continue

            if match['status']['shortName'] == 'Bşl':
                continue
            if match['status']['shortName'] == 'MS':
                match_object.done = True
                match_object.minute = 'ms'
                reward_punish_users.delay(match_object.id)
            if match['status']['shortName'] == 'İY':
                match_object.minute = 'iy'
                match_object.home_team_score = match['homeTeam']['score']['current']
                match_object.away_team_score = match['awayTeam']['score']['current']
                match_object.home_first_half_score = match['homeTeam']['score']['current']
                match_object.away_first_half_score = match['awayTeam']['score']['current']
            if match['status']['shortName'] == '1.Y':
                match_object.home_team_score = match['homeTeam']['score']['current']
                match_object.away_team_score = match['awayTeam']['score']['current']
                match_object.minute = str(calculate_minute(match['gameStartedDate']))
            if match['status']['shortName'] == '2.Y':
                match_object.home_team_score = match['homeTeam']['score']['current']
                match_object.away_team_score = match['awayTeam']['score']['current']
                match_object.minute = str(calculate_minute(match['secondHalfStartedDate']) + 45)
            match_object.save()


@task()
def reward_punish_users(match_id):
    match = Match.objects.get(id=match_id)
    today = datetime.today()
    highscores = Leaderboard('highscores')
    monthly_highscores = Leaderboard(str(today.month) + '-' + str(today.year) + '_highscores')
    score_total = match.home_team_score + match.away_team_score
    games = Game.objects.filter(match=match)
    odds = {}
    for game in games:
        odds[game.string] = game.odd
    winning_games = []
    # MS1 MSX MS2 CS1-X CS2-X CS1-2
    if match.home_team_score > match.away_team_score:
        winning_games.append('ms1')
        winning_games.append('cs1-x')
        winning_games.append('cs1-2')
    elif match.away_team_score > match.home_team_score:
        winning_games.append('ms2')
        winning_games.append('cs2-x')
        winning_games.append('cs1-2')
    else:
        winning_games.append('msx')
        winning_games.append('cs1-x')
        winning_games.append('cs2-x')
    # H1 HX H2
    home_score = match.home_team_score
    away_score = match.away_team_score
    if match.handicap == "0":
        pass
    elif match.handicap.startswith("-"):
        away_score = away_score + int(match.handicap[-1])
        if home_score > away_score:
            winning_games.append("h1")
        elif away_score > home_score:
            winning_games.append("h2")
        else:
            winning_games.append("hx")
    else:
        home_score = home_score + int(match.handicap)
        if home_score > away_score:
            winning_games.append("h1")
        elif away_score > home_score:
            winning_games.append("h2")
        else:
            winning_games.append("hx")
    # KGVAR KGYOK
    if match.home_team_score > 0 and match.away_team_score > 0:
        winning_games.append('kgvar')
    else:
        winning_games.append('kgyok')
    # TEK CIFT
    if score_total % 2 == 0:
        winning_games.append('tccift')
    else:
        winning_games.append('tctek')
    # TG 0-1 2-3 4-6 7+
    if score_total < 2:
        winning_games.append('tg0-1')
    elif score_total < 4:
        winning_games.append('tg2-3')
    elif score_total < 7:
        winning_games.append('tg4-6')
    else:
        winning_games.append('tg7+')
    # 1.5 ALT UST
    if score_total < 2:
        winning_games.append('au1,5-alt')
    else:
        winning_games.append('au1,5-ust')
    # 2.5 ALT UST
    if score_total < 3:
        winning_games.append('au2,5-alt')
    else:
        winning_games.append('au2,5-ust')
    # 3.5 ALT UST
    if score_total < 4:
        winning_games.append('au3,5-alt')
    else:
        winning_games.append('au3,5-ust')
    # IY 1.5 ALT UST
    if (match.home_first_half_score + match.away_first_half_score) < 2:
        winning_games.append('iyau1,5-alt')
    else:
        winning_games.append('iyau1,5-ust')
    # IY1 IY0 IY2
    if match.home_first_half_score > match.away_first_half_score:
        winning_games.append("iy1")
    elif match.home_first_half_score == match.away_first_half_score:
        winning_games.append("iy0")
    else:
        winning_games.append("iy2")
    # IY/MS
    if match.home_first_half_score > match.away_first_half_score:
        if match.home_team_score > match.away_team_score:
            winning_games.append("iyms1/1")
        elif match.home_team_score == match.away_team_score:
            winning_games.append("iyms1/x")
        else:
            winning_games.append("iyms1/2")
    elif match.home_first_half_score == match.away_first_half_score:
        if match.home_team_score > match.away_team_score:
            winning_games.append("iymsx/1")
        elif match.home_team_score == match.away_team_score:
            winning_games.append("iymsx/x")
        else:
            winning_games.append("iymsx/2")
    else:
        if match.home_team_score > match.away_team_score:
            winning_games.append("iyms2/1")
        elif match.home_team_score == match.away_team_score:
            winning_games.append("iyms2/x")
        else:
            winning_games.append("iyms2/2")
    # Rewarding and punishing users
    for game in GAMES_LIST:
        if game in winning_games:
            predictions = Prediction.objects.filter(game=game, match=match)
            for prediction in predictions:
                user = User.objects.get(id=prediction.user.id)
                user.skill_point = user.skill_point + odds[game] * 10.0

                # Updating all time leaderboard
                highscores.rank_member(user.id, user.skill_point)
                # Updating monthly leaderboard
                monthly = MonthlyScore.objects.filter(month__month=today.month)
                if monthly.exists():
                    monthly = monthly.first()
                    monthly.skill_point += odds[game] * 10.0
                    monthly.save()
                else:
                    monthly = MonthlyScore.objects.create(user=user, skill_point=(odds[game] * 10.0), month=today)
                monthly_highscores.rank_member(user.id, monthly.skill_point)

                user.save()

                # Trophy progression
                successful_predictions = SuccessCount.objects.filter(user=user, league=match.league)
                if successful_predictions.exists():
                    successful_predictions = successful_predictions.first()
                    successful_predictions.count += 1
                    successful_predictions.save()
                    trophy_type = TrophyType.objects.filter(league=match.league, count=successful_predictions.count)
                    if trophy_type.exists():
                        trophy_type = trophy_type.first()
                        Trophy.objects.create(
                            user=user,
                            text=trophy_type.text,
                            league=trophy_type.league,
                            description=trophy_type.description,
                            image=trophy_type.image
                        )
                else:
                    SuccessCount.objects.create(user=user, league=match.league, count=1)
        else:
            predictions = Prediction.objects.filter(game=game)
            for prediction in predictions:
                user = User.objects.get(id=prediction.user.id)
                user.skill_point = user.skill_point - odds[game] * 0.1
                highscores.rank_member(user.id, user.skill_point)
                user.save()
                monthly = MonthlyScore.objects.filter(month__month=today.month)
                if monthly.exists():
                    monthly = monthly.first()
                    monthly.skill_point += odds[game] * -0.1
                    monthly.save()
                else:
                    monthly = MonthlyScore.objects.create(user=user, skill_point=(odds[game] * -0.1), month=today)
                monthly_highscores.rank_member(user.id, monthly.skill_point)
    return winning_games
