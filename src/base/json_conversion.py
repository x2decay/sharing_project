from src.base.playvs_objects import Team
import json


def to_classes(file):
    teams = {}
    for (team_name, team) in json.load(file).items():
        print(team)
        players = team.pop('players')
        print(players)
        teams[team_name] = Team(team, from_json=True)
        for (player_name, data) in players.items():
            teams[team_name].add_series(player_name, data['series'], data['games'])
    return teams


def from_classes(teams):
    file = ''
    return file
