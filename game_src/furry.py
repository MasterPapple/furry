from random import randint
from stats import Attributes, Stats

class Furry:
    def __init__(self, name):
        self.name = name

        self.stats = Stats(10, 10, 2)
        self.attributes = Attributes()

    def attack(self, game, session):
        hero = session.hero
        if hero.attributes.defending:
            hero.stats.health = round(hero.stats.health - 0.4 * self.stats.strength, 2)
            hero.attributes.defending = False
        else:
            hero.stats.health -= self.stats.strength
        if hero.stats.health <= 0:
            game.send("FUCK!! A furry just killed you!")
            quit()
        game.send(f"furry_attack%{self.name}%{self.stats.strength}%{self.stats.health}/{self.stats.max_health}%{hero.stats.health}/{hero.stats.max_health}%{', '.join([act.name for act in hero.avail_actions])}")

