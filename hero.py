from os import name
from random import randint
from stats import Stats, Attributes

class Hero:

    class Action:
        def __init__(self, name, shortname, method, level=1) -> None:
            self.name = name
            self.shortname = shortname
            self.method = method
            self.unlocked_at = level

    def __init__(self, name):
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 10
        self.name = name
        self.weapon = None
        self.actions = [self.Action("damage", "d", self.action_damage),
                        self.Action("defend", "de", self.action_defend, 2),
                        self.Action("shop", "s", self.action_shop),
                        self.Action("rest", "r", self.action_rest)]
        self.avail_actions = []
        self.stats = Stats(20, 20, 3)
        self.attributes = Attributes()


    def take_action(self, game, session, action):        
        action.lower()

        for i_act in self.avail_actions:
            if action == i_act.name or action == i_act.shortname:
                return i_act.method(game, session)

        game.send("Invalid action")
        return True


    def actions_get(self, name):
        for i_act in self.actions:
            if i_act.name == name:
                return i_act


    def remove_actions(self, list):
        for action_name in list:
            action = self.actions_get(action_name)
            if action in self.avail_actions:
                self.avail_actions.remove(action)

    def set_actions(self, list):
        for action_name in list:
            action = self.actions_get(action_name)
            if action.unlocked_at <= self.level:
                self.avail_actions.append(action)


    def action_damage(self, game, session):
        furry = session.enemy
        furry.stats.health -= self.stats.strength #- self.weapon.strength
        game.send(f"You attacked the furry {furry.name} for {self.stats.strength} \nNow they have {furry.stats.health} health")
        if furry.stats.health <= 0:
            game.send("What a skilled hero, you are. You killed a furry.")
            self.remove_actions(["damage", "defend"])
            session.kill_furry()
            self.gain_experience(2, game)
        return False


    def action_defend(self, game, session):
        self.attributes.defending = True
        return False

    def action_flee(self):
        pass

    def action_victory_dance(self):
        # will be looting and fing furry as a victory reward
        pass

    def action_shop(self, game, session):
        self.weapon = weapon = session.weapon
        game.send(f"Succesfully bought {weapon.name}")
        self.remove_actions(["shop"])        
        return False

    def action_rest(self, game, session):
        pack = randint(1, 5)
        self.stats.health += pack
        game.send(f"You rested for {pack}")
        self.remove_actions(["rest"]) 
        return False

    def gain_experience(self, amount, game):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level += 1
            game.send(f"Leveled up to {self.level}")
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level = round (1.5 * self.experience_to_next_level)