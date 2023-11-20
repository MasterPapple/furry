
class Stats:
    def __init__(self, health, max_health, strength) -> None:
        self.health = health
        self.max_health = max_health
        self.strength = strength

class Attributes:
    def __init__(self) -> None:
        self.defending = False