import json
import sys
import os
from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.cache import caches
import requests
import django

# TODO: Change when deployed
sys.path.append("/root/mac-backend/")
os.environ['DJANGO_SETTINGS_MODULE'] = "mac.settings.staging"
django.setup()

from mac.forum.models import Match, Team, Game, League


GAMES = {
    'F.1': 'ms1',
    'F.X': 'msx',
    'F.2': 'ms2',
    'H15.U': 'iyau1,5-alt',
    'H15.O': 'iyau1,5-ust',
    'F15.U': 'au1,5-alt',
    'F15.O': 'au1,5-ust',
    'UNDER': 'au2,5-alt',
    'OVER': 'au2,5-ust',
    'F35.U': 'au3,5-alt',
    'F35.O': 'au3,5-ust',
    'S.1': 'iy1',
    'S.X': 'iyx',
    'S.2': 'iy2',
    'DC.1X': 'cs1-x',
    'DC.X2': 'csx-2',
    'DC.12': 'cs1-2',
    'H.1': 'h1',
    'H.2': 'h2',
    'H.X': 'hx',
    'SF.11': 'iyms1/1',
    'SF.1X': 'iyms1/x',
    'SF.12': 'iyms1/2',
    'SF.X1': 'iymsx/1',
    'SF.XX': 'iymsx/x',
    'SF.X2': 'iymsx/2',
    'SF.21': 'iyms2/1',
    'SF.2X': 'iyms2/x',
    'SF.22': 'iyms2/2',
    'SC.GG': 'kgvar',
    'SC.NG': 'kgyok',
    'GS.01': 'tg0-1',
    'GS.23': 'tg2-3',
    'GS.46': 'tg4-6',
    'GS.7P': 'tg7+'
}

r = requests.get('https://bulletin.iddaa.com/data/bulletin-with-percentage')
odds_json = json.loads(r.text)
IMAGE_URL = "https://cdn.broadage.com/images-teams/soccer/82x82/"

matches = odds_json['data']['bulletin']['football']['eventList']

dates = odds_json['data']['bulletin']['football']['meta']['dateList']
datelist = []

for date in dates:
    datelist.append(date['value'].replace('.', '-'))
caches['default'].set('dates', datelist)

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
    if Match.objects.filter(iddaa_id=match["id"]).exists():
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
        handicap=match["x"]
    )
    for odd in match['oddList']:
        if odd['type'] in GAMES:
            Game.objects.create(match=match_object, string=GAMES[odd["type"]], odd=float(odd["v"]))
