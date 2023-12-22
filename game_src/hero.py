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

    class Tech:
        def __init__(self, name, shortname) -> None:
            self.name = name
            self.shortname = shortname
            self.level = 0

    def __init__(self, name):
        self.level = 1
        self.skill_points = 0
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
        self.techtree = [self.Tech("knowledge", "k"), 
                         self.Tech("attack", "a"), 
                         self.Tech("shop", "s")]
        self.inventory = []
        self.i_capacity = 0

    def take_action(self, game, session, action):   

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
        furry.stats.health -= self.stats.strength #- self.weapon.strength game.send(f"You attacked the furry {furry.name} for {self.stats.strength} \nNow they have {furry.stats.health} health")
        if furry.stats.health <= 0:
            game.send(f"furry_kill")
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
        game.send(f"purchase%{weapon.name}")
        self.remove_actions(["shop"])        
        return False

    def action_rest(self, game, session):
        pack = randint(1, 5)
        self.stats.health += pack
        game.send(f"rest%{pack}")
        self.remove_actions(["rest"]) 
        return False

    def gain_experience(self, amount, game):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level += 1
            self.skill_points += 1
            game.send(f"Leveled up to {self.level} and gained a skill point")
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level = round (1.5 * self.experience_to_next_level)

    def upgrade_skill(self, skill, game):

        if self.skill_points <= 0:
            game.send("You don't have sufficient amount of skill points available!")
            return

        for branch in self.techtree:
            if skill == branch.name or skill == branch.shortname:
                branch.level += 1
                self.skill_points -= 1
                self.upgrade_changes(branch.name, branch.level)
                game.send(f"Upgraded {branch.name} to level {branch.level}")
                return
            
        game.send("Invalid skill")
        return
    
    def upgrade_changes(self, skill, level):
        if skill == "shop" and level == 2:
            self.i_capacity += 1

    def add_weapon(self, weapon, game):
        if self.weapon == None:
            self.weapon = weapon
            game.send("The purchased weapon has been equipped.")
        elif len(self.inventory) < self.i_capacity:
            self.inventory.append(weapon)
            game.send("The purchased weapon has been put into your inventory.")
        else:
            game.send("You have no free inventory capacity. Type 'c' to discard currently bought item or type 'w' or the number of your inventory slot to replace your current item.")