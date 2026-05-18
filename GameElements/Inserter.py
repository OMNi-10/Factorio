from utils import readJSON

from Quality import Quality
from ModelElements.config import CONFIG_PATH

CAPACITY_UPGRADE: int

class Inserter:
    type : str
    quality : Quality

    ticks_per_turn : int
    capacity : int

    energy_per_cycle : float # kJ/opertion
    passive_drain : float    # kW

    def __init__(self, type: str, quality: Quality = Quality.NORMAL):
        data = readJSON(CONFIG_PATH)
        inserters = data["inserters"]

        if type not in inserters:
            raise ValueError(f"Inserter type '{type}' not supported")

        inserter_data = inserters[type]
        self.type = type
        self.ticks_per_turn = inserter_data["ticks_per_turn"]
        self.capacity = inserter_data["capacity_upgrades"][CAPACITY_UPGRADE]
        self.quality = quality
        self.energy_per_cycle = inserter_data["energy_per_transfer"]
        self.passive_drain = inserter_data["drain"]

    def speed(self) -> float:
        base_speed = 360 * 60/self.ticks_per_turn
        return (1 + 0.3 * self.quality.value) * base_speed

    def items_per_second(self) -> float:
        turns_per_second = self.speed() / 360
        return turns_per_second * self.capacity


if __name__ == "__main__":
    CONFIG_PATH = "../config/space_age.json"
    CAPACITY_UPGRADE = 7
    inserter = Inserter("inserter")
    print(inserter.items_per_second())
    print(inserter.energy_per_cycle)