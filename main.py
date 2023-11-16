from random import randint, random

print(f"-=== Welcome to the League of Furries ===-")
print(f"Your task is simple. Kill them all!")


class Hero:
    def __init__(self, name):
        self.level = 1
        self.name = name
        self.health = (20, 20)
        self.weapon = None
        self.strength = 1
        self.avail_actions = ["damage"]

    def take_action(self, furry):
        action = input(f"Choose your preferred action ({', '.join(self.avail_actions)}) ")
        action.lower()
        if self.validate_action(action, "damage", "d") and not furry == None:
            self.action_damage(furry)
        elif self.validate_action(action, "defend", "de"):
            self.action_defend()
        else:
            print("Invalid action")
            self.take_action(furry)

    def validate_action(self, action, name, shortname):
        return (action == name or action == shortname) and name in self.avail_actions

    def action_damage(self, furry):
        furry.health -= self.strength #- self.weapon.strength
        print(f"You attacked the furry {furry.name} for {self.strength}")
        if furry.health <= 0:
            print("What a skilled hero, you are. You killed a furry.")
            furry.die()

    def action_defend(self):
        pass

    def action_flee(self):
        pass

    def action_victory_dance(self):
        # will be looting and fing furry as a victory reward
        pass

    def action_shop(self):
        pass

class Furry:
    def __init__(self, name):
        self.name = name
        self.health = 9 + randint(hero.level, hero.level**2)
        self.damage = 3

    def attack(self, hero):
        hero.health = (hero.health[0] - self.damage, hero.health[1])
        print(f"Furry {self.name} attacked you for {self.damage}")

    def die(self):
        global enemy
        enemy = None

class EventHandler:

    class Event:
        def __init__(self, type, chance, method) -> None:
            self.type = type
            self.chance = chance
            self.method = method

        def trigger(self):
            self.method()

    def __init__(self) -> None:
        self.all_events = []
        self.all_events.append(self.Event("furry_spawn", 1, spawn_furry))

        self.active_events = self.all_events

    def change_chance(self, type, new_chance):
        for event in self.active_events:
            if event.type != type:
                continue
            event.chance = new_chance
            self.active_events[self.active_events.index(event)] = event
            return

        for event in self.all_events:
            if event.type != type:
                continue
            event.chance = new_chance
            self.active_events.append(event)
            return            

    def roll_event(self):
        sum = 0
        for event in self.active_events:
            sum += event.chance
        chance = randint(1, sum)
        for event in self.active_events:
            chance -= event.chance
            if chance <= 0:
                event.trigger()



def spawn_furry():
    global enemy
    enemy = Furry("Jojo")
    print("jojo spawned")


hero = Hero(input(f"What's your name? "))
handler = EventHandler()
enemy = None


while True:
    if not enemy:
        handler.roll_event()
    hero.take_action(enemy)
    if not enemy == None:
        enemy.attack(hero)