from src.base.playvs_objects import Team
import json


def to_class(file):
    team = json.load(file)
    print(team)
    players = team.pop('players')
    print(players)
    team = Team(team, from_json=True)
    for (player_name, data) in players.items():
        team.add_series(player_name, data['series'], data['games'])
    return team


def from_class(team):
    file = ''
    return file
