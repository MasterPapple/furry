from random import randint, random

from hero import Hero
from furry import Furry
from event_handler import EventHandler

print(f"-=== Welcome to the League of Furries ===-")
print(f"Your task is simple. Kill them all!")

class Game:
    def __init__(self) -> None:
        self.hero = Hero(input(f"What's your name? "))
        self.current_event = None
        self.enemy = None

    def initiate_handler(self):
        self.handler = EventHandler(self)

    def kill_furry(self):
        self.enemy = None



game = Game()
game.initiate_handler()


while True:
    
    if not game.enemy:
        game.current_event = game.handler.roll_event(game)
    game.hero.take_action(game)
    if not game.enemy == None:
        game.enemy.attack(game.hero)