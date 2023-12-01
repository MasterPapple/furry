from random import randint, random
import socket
import threading
from _thread import *

from hero import Hero
from event_handler import EventHandler

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
        self.server_socket.bind(('192.168.1.27', 8080))
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



game = Game()
game.initiate_connection()



shutdown = False
while not shutdown:
    response = game.client_socket.recv(1024).decode('utf-8')
    try:
        session = game.sessions[response.split("%")[0]]
    except:
        print("No session yet")
    response = response.split("%")[1]

    if response == "start":
        session = game.start_session()
        session.initiate_handler()

        game.send(f"Your name is {session.hero.name}")
        session.current_event = session.handler.roll_event(game, session)
        game.send(f"Choose your preferred action ({', '.join([act.name for act in session.hero.avail_actions])}) ")

    elif response == "terminate":
        shutdown = True

    elif response == "actions":
        game.send(f"Choose your preferred action ({', '.join([act.name for act in session.hero.avail_actions])}) ")

    elif response == "help":
        game.send("Available commands are **start, terminate, actions, help**")

    elif response == "amirite":
        game.send("yes you're completely right. Loen is total bitch useless whore, who cant even fuck an ant")

    elif response == "furry":
        game.send("Display furry")

    elif session.hero is not None:
        invalid = session.hero.take_action(game, session, response)

        if not invalid and not session.enemy == None:
            session.enemy.attack(game, session)
        if not invalid and not session.enemy:
            session.current_event = session.handler.roll_event(game, session)

        game.send(f"Choose your preferred action ({', '.join([act.name for act in session.hero.avail_actions])}) ")

    else:
        print(f"Unsuccessfuly handled response was {response}")




game.client_socket.close()
game.server_socket.close()