from utils import readJSON

from GameElements.Quality import Quality

from ModelElements.config import CONFIG_PATH

class Module:
    type : str
    quality : Quality

    base_speed_bonus : float
    quality_effects_speed : bool

    base_productivity_bonus : float
    quality_effects_productivity : bool

    base_energy_increase : float
    quality_effects_energy : bool

    base_quality_bonus : float
    quality_effects_quality : bool

    pollution_modifier : float

    def __init__(self, type: str, tier: int, quality: Quality = Quality.NORMAL):
        data = readJSON(CONFIG_PATH)
        modules = data["modules"]

        if type not in modules:
            raise ValueError(f"Module type '{type}' not supported")

        module_data = modules[type]

        self.type = type
        self.quality = quality

        self.base_speed_bonus = module_data["base_speed_bonus"][tier - 1]
        self.quality_effects_speed = module_data["quality_effects_speed"]

        self.base_productivity_bonus = module_data["base_productivity_bonus"][tier - 1]
        self.quality_effects_productivity = module_data["quality_effects_productivity"]

        self.base_energy_increase = module_data["base_energy_increase"][tier - 1]
        self.quality_effects_energy = module_data["quality_effects_energy"]

        self.base_quality_bonus = module_data["base_quality_bonus"][tier - 1]
        self.quality_effects_quality = module_data["quality_effects_quality"]

        self.pollution_modifier = module_data["pollution_modifier"][tier - 1]

    def speed_modifier(self):
        if self.quality_effects_speed:
            return (1 + self.quality.value * 0.3) * self.base_speed_bonus
        else:
            return self.base_speed_bonus

    def productivity_modifier(self):
        if self.quality_effects_productivity:
            return (1 + self.quality.value * 0.3) * self.base_productivity_bonus
        else:
            return self.base_productivity_bonus

    def energy_modifier(self):
        if self.quality_effects_energy:
            return (1 + self.quality.value * 0.3) * self.base_energy_increase
        else:
            return self.base_energy_increase

    def quality_modifier(self):
        if self.quality_effects_quality:
            return (1 + self.quality.value * 0.3) * self.base_quality_bonus
        else:
            return self.base_quality_bonus


if __name__ == "__main__":
    CONFIG_PATH = "../config/space_age.json"
    module = Module(type="speed", tier=3, quality=Quality.LEGENDARY)
    print(module.speed_modifier())
    print(module.productivity_modifier())
    print(module.energy_modifier())
    print(module.quality_modifier())
