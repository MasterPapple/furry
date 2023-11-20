from stats import Stats, Attributes

class Hero:
    def __init__(self, name):
        self.level = 1
        self.name = name
        self.weapon = None
        self.avail_actions = ["damage", "defend"]
        self.stats = Stats(20, 20, 1)
        self.attributes = Attributes()

    def take_action(self, furry):
        action = input(f"Choose your preferred action ({', '.join(self.avail_actions)}) ")
        action.lower()
        if self.validate_action(action, "damage", "d") and not furry == None:
            return self.action_damage(furry)
        elif self.validate_action(action, "defend", "de"):
            self.action_defend()
        else:
            print("Invalid action")
            self.take_action(furry)

    def validate_action(self, action, name, shortname):
        return (action == name or action == shortname) and name in self.avail_actions

    def action_damage(self, furry):
        furry.stats.health -= self.stats.strength #- self.weapon.strength
        print(f"You attacked the furry {furry.name} for {self.stats.strength} \nNow they have {furry.stats.health} health")
        if furry.stats.health <= 0:
            print("What a skilled hero, you are. You killed a furry.")
            furry = furry.die()
        return furry

    def action_defend(self):
        self.attributes.defending = True

    def action_flee(self):
        pass

    def action_victory_dance(self):
        # will be looting and fing furry as a victory reward
        pass

    def action_shop(self):
        pass