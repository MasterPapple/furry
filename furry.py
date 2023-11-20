from random import randint
from stats import Attributes, Stats

class Furry:
    def __init__(self, name):
        self.name = name

        self.stats = Stats(10, 10, 2)
        self.attributes = Attributes()

    def attack(self, hero):
        hero.stats.health = hero.stats.health - self.stats.strength
        if hero.stats.health <= 0:
            print("FUCK!! A furry just killed you!")
            quit()
        print(f"Furry {self.name} attacked you for {self.stats.strength} \nAnd you have {hero.stats.health} left")

    def die(self):
        return None