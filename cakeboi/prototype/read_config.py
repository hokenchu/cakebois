import json


def get(key):
    with open("config.json", "r") as read_file:
        return json.load(read_file)[key]
