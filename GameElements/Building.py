from enum import Enum

from GameElements.Module import Module
from GameElements.Quality import Quality
from utils import readJSON

from ModelElements.config import CONFIG_PATH

class Category(Enum):
    EXTRACTOR = "extractor"
    FURNACE = "furnace"
    TRANSFORMER = "transformer"


class Building:
    type : str
    category : Category
    quality : Quality

    # Production
    base_speed : float
    base_productivity : float
    base_quality: float
    handles_fluids : bool

    # Energy
    is_burner : bool
    base_consumption : float  # kW
    base_pollution : float
    drain: float  # kW

    # Modules
    module_slots: int
    modules: list[Module]
    # beacon_modules: list[Module]

    def __init__(self, type : str, quality : Quality = Quality.NORMAL, modules : list[Module] = None):
        self.type = type
        self.quality = quality

        data = readJSON(CONFIG_PATH)
        buildings = data["buildings"]

        if type not in buildings:
            raise ValueError(f"Building type '{type}' not supported")

        building_data = buildings[type]
        self.base_speed = building_data["base_speed"]
        self.base_productivity = building_data["base_productivity"]
        self.base_quality = building_data["base_quality"]
        self.handles_fluids = building_data["handles_fluids"]

        self.is_burner = building_data["is_burner"]
        self.base_consumption = building_data["base_consumption"]
        self.base_pollution = building_data["base_pollution"]
        self.drain = building_data["drain"]

        self.module_slots = building_data["module_slots"]

        if modules is None:
            self.modules = []
        else:
            assert(len(modules) <= self.module_slots), f"There may not be more than {self.module_slots} modules in building type {type}"
            self.modules = modules

    def crafting_speed(self) -> float:
        crafting_speed = self.base_speed
        for module in self.modules:
            crafting_speed += 1 - module.speed_modifier()
        return crafting_speed

    def productivity(self) -> float:
        productivity = self.base_productivity
        for module in self.modules:
            productivity += module.productivity_modifier()
        return productivity

    def energy_modifier(self) -> float:
        energy_modifier = 1
        for module in self.modules:
            energy_modifier += 1 - module.energy_modifier()
        return max(energy_modifier, 0.2)

    def quality_chance(self) -> float:
        quality_chance = self.base_quality
        for module in self.modules:
            quality_chance += 1 - module.quality_modifier()
        return quality_chance

    def energy_consumption(self) -> float:
        return self.base_consumption * self.energy_modifier() + self.drain


if __name__ == "__main__":
    CONFIG_PATH = "../config/space_age.json"
    building = Building("assembly_machine_3")

    print(building.energy_consumption())