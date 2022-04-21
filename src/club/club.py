from multiprocessing.dummy import Process
import os
from os.path import exists

from src.club.player import Player
from src.match.match_report import MatchReport
from src.utilities.data_utilities import *

PLAYER_FILE = "/players.txt"
REPORT_FILE = "/reports.txt"

class Club:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.match_reports = []

    def LoadPlayers(self, folder):
        if os.path.exists(folder + PLAYER_FILE):
            with open(folder + PLAYER_FILE, "r") as source:
                for player_data in source:
                    loaded_player = Player()
                    loaded_player.Load(ProcessData(player_data))
                    self.players.append(loaded_player)
        self.players.sort()
        
    def LoadMatchReports(self, folder):
        if os.path.exists(folder + REPORT_FILE):
            with open(folder + REPORT_FILE) as source:
                for report_data in source:
                    new_report = MatchReport()
                    new_report.Load(report_data)
                    self.AddMatchReport(new_report)


    def SaveClub(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        SaveObjects(folder + PLAYER_FILE, self.players)
        SaveObjects(folder + REPORT_FILE, self.match_reports)

    def Load(self, folder):
        self.LoadPlayers(folder)
        self.LoadMatchReports(folder)

    def AddPlayer(self, name):
        new_player = Player(name)
        self.players.append(new_player)
        self.players.sort()
    
    def AddMatchReport(self, report):
        self.match_reports.append(report)

    def RemovePlayer(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                break
        self.players.sort()


