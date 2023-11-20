from random import randint, random

from hero import Hero
from furry import Furry

print(f"-=== Welcome to the League of Furries ===-")
print(f"Your task is simple. Kill them all!")




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
    file = open("furry_names.txt")
    lines = file.readlines()
    name = lines[randint(1, 100)].strip()
    enemy = Furry(name)
    print(f"{name} spawned")


hero = Hero(input(f"What's your name? "))
handler = EventHandler()
enemy = None


while True:
    if not enemy:
        handler.roll_event()
    enemy = hero.take_action(enemy)
    if not enemy == None:
        enemy.attack(hero)