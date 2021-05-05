import json


def key_json(path):
    jOpen = open(path)
    # with open(path) as f:
    return json.load(jOpen)
