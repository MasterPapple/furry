from os import name
from random import randint
from stats import Stats, Attributes

class Hero:

    class Action:
        def __init__(self, name, shortname, method) -> None:
            self.name = name
            self.shortname = shortname
            self.method = method

    def __init__(self, name):
        self.level = 1
        self.name = name
        self.weapon = None
        self.actions = []
        self.actions.extend([self.Action("damage", "d", self.action_damage),
                            self.Action("defend", "de", self.action_defend),
                            self.Action("shop", "s", self.action_shop),
                            self.Action("rest", "r", self.action_rest)])
        self.avail_actions = []
        self.stats = Stats(20, 20, 3)
        self.attributes = Attributes()


    def take_action(self, game):
        action = input(f"Choose your preferred action ({', '.join([act.name for act in self.avail_actions])}) ")
        action.lower()
        for i_act in self.avail_actions:
            if action == i_act.name or action == i_act.shortname:
                return i_act.method(game)
        print("Invalid action")
        self.take_action(game)


    def actions_get(self, name):
        for i_act in self.actions:
            if i_act.name == name:
                return i_act


    def action_damage(self, game):
        furry = game.enemy
        furry.stats.health -= self.stats.strength #- self.weapon.strength
        print(f"You attacked the furry {furry.name} for {self.stats.strength} \nNow they have {furry.stats.health} health")
        if furry.stats.health <= 0:
            print("What a skilled hero, you are. You killed a furry.")
            self.avail_actions.remove(self.actions_get("damage"))
            self.avail_actions.remove(self.actions_get("defend"))
            game.kill_furry()
        return 
        

    def action_defend(self, game):
        self.attributes.defending = True
        return 

    def action_flee(self):
        pass

    def action_victory_dance(self):
        # will be looting and fing furry as a victory reward
        pass

    def action_shop(self, game):
        self.weapon = weapon = game.weapon
        print(f"Succesfully bought {weapon.name}")
        self.avail_actions.remove(self.actions_get("shop"))
        return weapon

    def action_rest(self, game):
        pack = randint(1, 5)
        self.stats.health += pack
        print(f"You rested for {pack}")
        self.avail_actions.remove(self.actions_get("rest"))
        return