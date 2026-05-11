from enum import Enum

class Quality(Enum):
    NORMAL = 0
    UNCOMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 5

if __name__ == "__main__":
    print(Quality.NORMAL.value)