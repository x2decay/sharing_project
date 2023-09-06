from src.base.playvs_objects import Team
import json


def to_object(file):
    team = json.load(file)
    players = team.pop('players')
    team = Team(team, from_json=True)
    for player in players:
        for series in player['series']:
            team.add_series(player['name'], series['number'], series['games'])
    return team


def from_object(team):
    dictionary = {'name': team.name, 'school': team.school, 'href': team.href}
    players = []
    for player in team.players:
        p = {'name': player.name, 'series': []}
        for series in player.series:
            p['series'].append({'number': series.number, 'games': [g.list() for g in series.games]})
        players.append(p)
    dictionary['players'] = players
    return json.dumps(dictionary, indent=2)
