from playvs_objects import *
import json


def to_classes(file):
    j = json.load(file)
    out = {}
    for team in json:
        data = []
        out[team['name']] = Team(raw_data=data, from_json=True)


def from_classes():
    pass
