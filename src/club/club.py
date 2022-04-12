import os
from os.path import exists

from src.club.player import Player
from src.utilities.data_utilities import *

class Club:

    def __init__(self):
        self.players = []

    def LoadPlayers(self, file):
        if os.path.exists(file):
            with open(file, "r") as source:
                for player_data in source:
                    loaded_player = Player()
                    loaded_player.Load(ProcessData(player_data))
                    self.players.append(loaded_player)
        self.players.sort()

    def SaveClub(self, file):
        SaveObjects(file, self.players)

    def AddPlayer(self, name):
        new_player = Player()
        new_player.name = name
        self.players.append(new_player)
        self.players.sort()

    def RemovePlayer(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                break
        self.players.sort()


