import json

def readJSON(path: str):
    with open(path, "r") as f:
        return json.load(f)