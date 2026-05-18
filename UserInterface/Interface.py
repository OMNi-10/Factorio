from GameElements.Building import Building
from utils import readJSON

from GameElements.Resource import Resource
from GameElements.Recipe import Recipe

from ModelElements.ResourceFlow import ResourceFlow
from ModelElements.Process import Process


if __name__ == "__main__":
    CONFIG_PATH = "../config/space_age.json"
else:
    from ModelElements.config import CONFIG_PATH

def prompt_user(prompt, options: dict[str, str] = None) -> str:
    if options is None:
        options = {}
    print(f"\n{prompt}")
    for key, value in options.items():
        print(f"\t - {key}: {value}")
    print(" >>> ", end="")
    response = input()
    return response

def process_prompt(prompt: str, valid_options: dict[str, str]) -> str:
    while True:
        response = prompt_user(prompt, valid_options)
        if response in valid_options.values():
            return response
        elif response in valid_options:
            response = valid_options[response]
            return response
        else:
            print("Unrecognized option. Please try again.")

def options_from_list(objects: list[str]) -> dict[str, str]:
    object_dict = {}
    for i in range(len(objects)):
        object_dict[str(i+1)] = objects[i]
    return object_dict

def find_valid_recipes(item: Resource) -> list[Recipe]:
    data = readJSON(CONFIG_PATH)
    recipe_list = data["recipes"]
    valid_recipes = []
    for recipe_name in recipe_list:
        if item.name in recipe_list[recipe_name]["outputs"]:
            valid_recipes.append(Recipe(recipe_name))
    return valid_recipes

class Interface:
    targets : list[ResourceFlow]
    def __init__(self):
        pass

    def add_target(self):

        response = process_prompt("")

if __name__ == "__main__":
    data = readJSON(CONFIG_PATH)
    valid_items = options_from_list(data["resources"])
    item_name = process_prompt("What resource would you like to produce?", valid_items)

    rate = float(prompt_user("How much would you like to process per second?"))

    target = ResourceFlow(item_name, rate)

    valid_recipes = find_valid_recipes(Resource(item_name))
    valid_recipe_names = options_from_list([recipe.name for recipe in valid_recipes])
    recipe_name = process_prompt("What recipe would you like to use?", valid_recipe_names)
    recipe = Recipe(recipe_name)

    processor_name = process_prompt("What building would you like to use?", options_from_list(recipe.valid_processors))
    processor: Building = Building(processor_name)

    process = Process(recipe, target, processor)
    print(process.building_count())
    inputs = process.inputs()
    for input in inputs:
        print(f"{input.rate} x {input.resource.name}")




