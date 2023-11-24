from random import randint
from furry import Furry
from weapon import get_random_weapon

class EventHandler:

    class Event:
        def __init__(self, type, chance, method, act_list) -> None:
            self.type = type
            self.chance = chance
            self.method = method
            self.actions = act_list


    def __init__(self, game) -> None:

        self.all_events = []
        self.all_events.append(self.Event("furry_spawn", 1, spawn_furry, [game.hero.actions_get(name) for name in ["damage", "defend"]]))
        self.all_events.append(self.Event("merchant_spawn", 1, spawn_merchant, [game.hero.actions_get("shop")]))
        self.all_events.append(self.Event("inn_visit", 1, visit_inn, [game.hero.actions_get("rest")]))

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


    def roll_event(self, game):

        sum = 0
        for event in self.active_events:
            sum += event.chance
        chance = randint(1, sum)
        for event in self.active_events:
            chance -= event.chance
            if chance <= 0:
                return_event = (event.type, event.method(game))
                game.hero.avail_actions.extend(event.actions)
                chance = 1000
                self.change_chance(event.type, 1)
            else:
                self.change_chance(event.type, event.chance + 1)

        return return_event


def spawn_furry(game):

    file = open("furry_names.txt")
    lines = file.readlines()
    name = lines[randint(1, 100)].strip()
    enemy = Furry(name)
    print(f"{name} spawned")
    game.enemy = enemy

def spawn_merchant(game):

    weapon = get_random_weapon()    
    print("You found a wandering merchant")
    game.weapon = weapon

def visit_inn(game):

    print("You walk by an inn")
    return 1