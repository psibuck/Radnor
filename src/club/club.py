from multiprocessing.dummy import Process
import os, json
from os.path import exists

from src.club.player import Player
from src.match.match_report import MatchReport
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import *

CLUB_FILE = "/club.json"
PLAYER_FILE = "/players.json"
MATCH_REPORTS_FILE = "/match_reports.json"
TRAINING_REPORTS_FILE = "/training_reports.json"
TRAINING_VENUES_FILE = "/training_venues.json"

class Club:

    def __init__(self, name):
        self.name = name

        # Before these were explicit to avoid adding incorrect objects
        # investigate why this fails in load from json
        self.players = []
        self.match_reports = []
        self.training_reports = []
        self.training_venues = []
        self.opponents = []

    def SaveClub(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        SaveObjectToJson(folder + CLUB_FILE, self)
        SaveToJson(folder + PLAYER_FILE, self.players)
        SaveToJson(folder + MATCH_REPORTS_FILE, self.match_reports)
        SaveToJson(folder + TRAINING_VENUES_FILE, self.training_venues)
        SaveToJson(folder + TRAINING_REPORTS_FILE, self.training_reports)

    def Load(self, folder):
        LoadObjectFromJson(folder + CLUB_FILE, self)
        LoadFromJson(folder + PLAYER_FILE, Player, self.players)
        LoadFromJson(folder + MATCH_REPORTS_FILE, MatchReport, self.match_reports)
        LoadFromJson(folder + TRAINING_VENUES_FILE, TrainingVenue, self.training_venues)
        LoadFromJson(folder + TRAINING_REPORTS_FILE, TrainingReport, self.training_reports)

        self.ProcessMatchReports()
        self.ProcessTrainingReports()

    def AddPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return False, "Player must have distinct name"
        new_player = Player(name)
        self.players.append(new_player)
        self.players.sort()
        return True, None
    
    def AddMatchReport(self, report):
        self.match_reports.append(report)
        self.ProcessMatchReport(report)

    def AddTrainingReport(self, report):
        self.training_reports.append(report)
        self.ProcessTrainingReport(report)

    def RemovePlayer(self, player):
        self.players.remove(player)
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

    def AddOpponent(self, opponent):
        self.opponents.append(opponent)
        self.opponents.sort()
    
    def FromJson(self, json_data):
        self.name = JsonGet(json_data, "name")
        self.opponents = JsonGet(json_data, "opponents")

    def ToJson(self):
        return {
            "name": self.name,
            "opponents": self.opponents
        }

        