from enum import Enum

from Module import Module
from Quality import Quality

CONFIG_PATH : str

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

    def crafting_speed(self) -> float:
        crafting_speed = self.base_crafting_speed
        for module in self.modules:
            crafting_speed += 1 - module.speed_modifier()
        return crafting_speed

    def productivity(self) -> float:
        productivity = self.base_productivity
        for module in self.modules:
            productivity += 1 - module.productivity_modifier()
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