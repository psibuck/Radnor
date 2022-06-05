import os

from src.club.club import Club
from src.club.player import Player
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.match.fixture import Fixture
from src.match.match_report import MatchReport
from src.utilities.data_utilities import *
from ui.page_manager import PageManager

DATA_FOLDER = "data/local/"
CLUB_FILE = "/club.json"
FIXTURES_FILE = "/fixtures.json"
PLAYER_FILE = "/players.json"
MATCH_REPORTS_FILE = "/match_reports.json"
TRAINING_REPORTS_FILE = "/training_reports.json"
TRAINING_VENUES_FILE = "/training_venues.json"

class Application:

    def __init__(self):
        self.make_data_structure()

        self.club = Club("Radnor", self.handle_club_data_changed)
        self.load_club()
        self.ui = PageManager(self)
        
        self.is_running = True

    def make_data_structure(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/local"):
            os.mkdir("data/local")   

    def activate(self):
        self.ui.draw()

    def handle_club_data_changed(self):
        self.save_club()
        
    def save_club(self):
        folder = DATA_FOLDER + self.club.name
        if not os.path.exists(folder):
            os.mkdir(folder)
        save_object_to_json(folder + CLUB_FILE, self.club)
        save_to_json(folder + PLAYER_FILE, self.club.players)
        save_to_json(folder + FIXTURES_FILE, self.club.fixtures)
        save_to_json(folder + MATCH_REPORTS_FILE, self.club.match_reports)
        save_to_json(folder + TRAINING_VENUES_FILE, self.club.training_venues)
        save_to_json(folder + TRAINING_REPORTS_FILE, self.club.training_reports)

    def load_club(self):
        folder = DATA_FOLDER + self.club.name
        load_object_from_json(folder + CLUB_FILE, self.club)
        load_from_json(folder + PLAYER_FILE, Player, self.club.players)
        load_from_json(folder + FIXTURES_FILE, Fixture, self.club.fixtures)
        load_from_json(folder + MATCH_REPORTS_FILE, MatchReport, self.club.match_reports)
        load_from_json(folder + TRAINING_VENUES_FILE, TrainingVenue, self.club.training_venues)
        load_from_json(folder + TRAINING_REPORTS_FILE, TrainingReport, self.club.training_reports)
    
    def quit(self):
        self.save_club()
        self.ui.shutdown()

# Refactor this, consider role of page manager vs app, same thing?
app = Application()
app.activate()