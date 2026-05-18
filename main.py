from GameElements.Building import Building
from GameElements.Quality import Quality
from GameElements.Recipe import Recipe
from GameElements.Module import Module

from ModelElements.ResourceFlow import ResourceFlow
from ModelElements.Process import Process


modules = []
building = Building("assembly_machine_2", modules=modules)

target = ResourceFlow("processing_unit", 6)
recipe = Recipe("processing_unit")
process = Process(recipe, target, building)

print(process.building_count())
inputs = process.inputs()
for input in inputs:
    print(f"{input.rate} x {input.resource.name}")