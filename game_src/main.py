from random import randint, random
import socket
from _thread import *
import time
import json

from hero import Hero
from event_handler import EventHandler
from tech_tree import TechTree

print(f"-=== Welcome to the League of Furries ===-")
print(f"Your task is simple. Kill them all!")

class Game:
    def __init__(self) -> None:
        self.client_socket = None
        self.server_socket = None
        self.client_adress = None
        self.sessions = {}

    class Session:
        def __init__(self, name) -> None:
            self.hero = Hero(name)
            self.current_event = None
            self.enemy = None

        def kill_furry(self):
            self.enemy = None

        def initiate_handler(self):
            self.handler = EventHandler(self)

    def initiate_connection(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('192.168.1.25', 8080))
        self.server_socket.listen(1)
        print(f"Server listening now")

        self.client_socket, self.client_adress = self.server_socket.accept()
        print(f"Connection from {self.client_adress}")

    def start_session(self):
        game.send("What's your name?")
        response = game.client_socket.recv(1024).decode('utf-8')
        resp_list = response.split("%")
        print(resp_list)
        self.sessions[resp_list[1]] = self.Session(resp_list[0])
        return self.sessions[resp_list[1]]

    def send(self, message):
        game.client_socket.send(str.encode(message))

    def save(self):
        primitives = (bool, str, int, float, type(None))
        hero_collect = {}
        for session in self.sessions.values():
            for attribute in session.hero.__dict__:
                if isinstance(attribute, primitives):
                    hero_collect[attribute] = session.hero.__dict__[attribute]

        print(hero_collect)


    def load(self):
        pass



game = Game()
tech_tree_gen = TechTree()
game.initiate_connection()



shutdown = False
while not shutdown:
    response = game.client_socket.recv(1024).decode('utf-8')
    try:
        session = game.sessions[response.split("%")[0]]
        response = response.lower()
    except:
        session = None
        print("No session yet")
    response = response.split("%")[1]


    if response == "start":
        session = game.start_session()
        session.initiate_handler()

        game.send(f"Your name is {session.hero.name}")
        time.sleep(0.2)
        session.current_event = session.handler.roll_event(game, session)

    elif response == "terminate":
        game.save()
        shutdown = True

    elif response == "help":
        game.send("help")

    elif response == "amirite":
        game.send("yes you're completely right. Loen is total bitch useless whore, who cant even fuck an ant")
        

    elif session is not None:

        if response == "inventory":
            game.send(f"inventory%{', '.join([item.name for item in session.hero.inventory])}") #finish

        elif response == "actions":
            game.send(f"actions%{', '.join([act.name for act in session.hero.avail_actions])}")

        elif response == "techtree" or response == "tt":
            tech_tree_gen.render(session)
            game.send(f"tech_tree%{session.hero.skill_points}")

        elif response == "skill":
            game.send("skill")

        elif response.split(' ')[0] == "skill":
            session.hero.upgrade_skill(response.split(' ')[1], game)

        elif response == "levelup" or response.split(' ')[0] == "levelup":
            if response == "levelup":
                level = 1
            else:
                level = int(response.split(' ')[1])
            session.hero.level += level
            session.hero.skill_points += level

        elif session is not None and session.hero is not None:
            output = session.hero.take_action(game, session, response)
            time.sleep(0.2)

            if not output and not session.enemy == None:
                session.enemy.attack(game, session)
            if not output and not session.enemy:
                session.current_event = session.handler.roll_event(game, session)

    else:
        print(f"Unsuccessfuly handled response was {response}")




game.client_socket.close()
game.server_socket.close()