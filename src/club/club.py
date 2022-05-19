from multiprocessing.dummy import Process
import os
from os.path import exists

from src.club.player import Player
from src.match.match_report import MatchReport
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import *

PLAYER_FILE = "/players.txt"
MATCH_REPORTS_FILE = "/match_reports.txt"
TRAINING_REPORTS_FILE = "/training_reports.txt"
TRAINING_VENUES_FILE = "/training_venues.txt"

class Club:

    def __init__(self, name):
        self.name = name
        self.players = []
        self.match_reports = list[MatchReport]
        self.training_reports = list[TrainingReport]
        self.training_venues = list[TrainingVenue]

    def LoadContent(self, folder, content_class, file):
        content_out = []
        if os.path.exists(folder + file):
            with open(folder + file, "r") as source:
                for data in source:
                    loaded_content = content_class()
                    loaded_content.Load(data)
                    content_out.append(loaded_content)
        return content_out
            
    def LoadPlayers(self, folder):
        if os.path.exists(folder + PLAYER_FILE):
            with open(folder + PLAYER_FILE, "r") as source:
                for player_data in source:
                    loaded_player = Player()
                    loaded_player.Load(ProcessData(player_data))
                    self.players.append(loaded_player)
        
    def LoadMatchReports(self, folder):
        if os.path.exists(folder + MATCH_REPORTS_FILE):
            with open(folder + MATCH_REPORTS_FILE) as source:
                for report_data in source:
                    new_report = MatchReport()
                    new_report.Load(report_data)
                    self.AddMatchReport(new_report)


    def SaveClub(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        SaveObjects(folder + PLAYER_FILE, self.players)
        SaveObjects(folder + MATCH_REPORTS_FILE, self.match_reports)
        SaveObjects(folder + TRAINING_REPORTS_FILE, self.training_reports)
        SaveObjects(folder + TRAINING_VENUES_FILE, self.training_venues)

    def Load(self, folder):
        # ordering matters here
        self.LoadPlayers(folder)
        self.match_reports = self.LoadContent(folder, MatchReport, MATCH_REPORTS_FILE)
        self.training_venues = self.LoadContent(folder, TrainingVenue, TRAINING_VENUES_FILE)
        self.training_reports = self.LoadContent(folder, TrainingReport, TRAINING_REPORTS_FILE)

        self.ProcessMatchReports()
        self.ProcessTrainingReports()

    def AddPlayer(self, name):
        new_player = Player(name)
        self.players.append(new_player)
        self.players.sort()
    
    def AddMatchReport(self, report):
        self.match_reports.append(report)
        self.ProcessMatchReport(report)

    def AddTrainingReport(self, report):
        self.training_reports.append(report)
        self.ProcessTrainingReport(report)

    def RemovePlayer(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
                break
        self.players.sort()

    def ProcessMatchReports(self):
        for report in self.match_reports:
            self.ProcessMatchReport(report)
    
    def ProcessMatchReport(self, report):
        for starter in report.starting_lineup:
            for player in self.players:
                if player.name == starter:
                    player.matches_started += 1
        for sub in report.subs:
            for player in self.players:
                if player.name == sub:
                    player.matches_as_sub += 1

    def ProcessTrainingReport(self, report):
        for attendee in report.attendees:
            for player in self.players:
                if player.name == attendee:
                    player.training_attendance += 1

    def ProcessTrainingReports(self):
        for report in self.training_reports:
            self.ProcessTrainingReport(report)

        