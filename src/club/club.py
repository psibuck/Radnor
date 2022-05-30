import os

from src.match.fixture import Fixture
from src.club.player import Player
from src.match.match_report import MatchReport
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import *

CLUB_FILE = "/club.json"
FIXTURES_FILE = "/fixtures.json"
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
        self.fixtures = []
        self.opponents = []

    def save_club(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)
        save_object_to_json(folder + CLUB_FILE, self)
        save_to_json(folder + PLAYER_FILE, self.players)
        save_to_json(folder + FIXTURES_FILE, self.fixtures)
        save_to_json(folder + MATCH_REPORTS_FILE, self.match_reports)
        save_to_json(folder + TRAINING_VENUES_FILE, self.training_venues)
        save_to_json(folder + TRAINING_REPORTS_FILE, self.training_reports)

    def load_club(self, folder):
        load_object_from_json(folder + CLUB_FILE, self)
        load_from_json(folder + PLAYER_FILE, Player, self.players)
        load_from_json(folder + FIXTURES_FILE, Fixture, self.fixtures)
        load_from_json(folder + MATCH_REPORTS_FILE, MatchReport, self.match_reports)
        load_from_json(folder + TRAINING_VENUES_FILE, TrainingVenue, self.training_venues)
        load_from_json(folder + TRAINING_REPORTS_FILE, TrainingReport, self.training_reports)

        self.process_match_reports()
        self.process_training_reports()

    def add_player(self, name):
        for player in self.players:
            if player.name == name:
                return False, "Player must have distinct name"
        new_player = Player(name)
        self.players.append(new_player)
        self.players.sort()
        return True, None
    
    def add_match_report(self, report):
        self.match_reports.append(report)
        self.process_match_report(report)

    def AddFixture(self, fixture):
        self.fixtures.append(fixture)

    def remove_fixture(self, fixture):
        self.fixtures.remove(fixture)

    def add_training_report(self, report):
        self.training_reports.append(report)
        self.process_training_report(report)

    def remove_player(self, player):
        self.players.remove(player)
        self.players.sort()

    def remove_match_report(self, report):
        self.match_reports.remove(report)
        self.process_match_report(report, False)

    def process_match_reports(self):
        for report in self.match_reports:
            self.process_match_report(report)
    
    def process_match_report(self, report, add=True):
        for starter in report.starting_lineup:
            for player in self.players:
                if player.name == starter:
                    if add:
                        player.matches_started += 1
                    else:
                        player.matches_started -= 1
        for sub in report.subs:
            for player in self.players:
                if player.name == sub:
                    if add:
                        player.matches_as_sub += 1
                    else:
                        player.matches_as_sub -= 1

    def process_training_report(self, report):
        for attendee in report.attendees:
            for player in self.players:
                if player.name == attendee:
                    player.training_attendance += 1

    def process_training_reports(self):
        for report in self.training_reports:
            self.process_training_report(report)

    def add_opponent(self, opponent):
        self.opponents.append(opponent)
        self.opponents.sort()
    
    def from_json(self, json_data):
        self.name = json_get(json_data, "name")
        self.opponents = json_get(json_data, "opponents")

    def to_json(self):
        return {
            "name": self.name,
            "opponents": self.opponents
        }

        