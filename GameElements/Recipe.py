from GameElements.Resource import Resource

from utils import readJSON

CONFIG_PATH : str

class Recipe:
    name : str
    inputs : dict[Resource, int]
    outputs : dict[Resource, int]
    duration : float
    valid_processors : list[str]

    def __init__(self, name : str):
        data = readJSON(CONFIG_PATH)
        recipes = data["recipes"]

        if name not in recipes:
            raise ValueError(f"Recipe named '{name}' not supported")

        recipe_data = recipes[name]
        self.name = name
        self.inputs = recipe_data["inputs"]
        self.outputs = recipe_data["outputs"]
        self.duration = recipe_data["duration"]
        self.valid_processors = recipe_data["valid_processors"]