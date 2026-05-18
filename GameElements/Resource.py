from utils import readJSON
from ModelElements.config import CONFIG_PATH

class Resource:
    name : str

    def __init__(self, name: str):
        data = readJSON(CONFIG_PATH)
        resources = data["resources"]

        if name not in resources:
            raise ValueError(f"Resource type '{name}' not supported")

        self.name = name