from random import randint, choice
from stats import Attributes, Stats
from pathlib import Path

class Furry:
            
    def __init__(self, name):
        self.name = name
        self.species = choice(["canis", "felis", "reptilia"])

        directory = "furry_images"

        files = Path(directory).glob('*')
        list = []
        for file in files:
            if self.species in file.name:
                list.append(file)
        image_no = randint(1, len(list)) - 1
        self.image_path = list[image_no]
        print(self.image_path)

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
            hero.weapon.decrease_durability(hero) #add deleveling and losing skills proportionatelly
            game.send(f"death")
            return
        messagestring = f"furry_attack%{self.name}%{self.stats.strength}%{self.stats.health}/{self.stats.max_health}"
        messagestring = messagestring + f"%{hero.stats.health}/{hero.stats.max_health}%{', '.join([act.name for act in hero.avail_actions])}"
        messagestring = messagestring + f"%{hero.stats.strength}"
        if hero.weapon == None:
            messagestring = messagestring + f"%None%0"
        else:
            messagestring = messagestring + f"%{hero.weapon.name}%{hero.weapon.attack_power}"
        if hero.techtree[0].level > 0:
            messagestring = messagestring + f"%{self.species}"
        else:
            messagestring = messagestring + f"%unidentified"
        game.send(messagestring)

