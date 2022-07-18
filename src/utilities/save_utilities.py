from src.utilities.data_utilities import *
from src.club.player import Player
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.match.fixture import Fixture
from src.match.match_report import MatchReport

DEBUG = 1

DATA_FOLDER = "C:/Users/psibu/Documents/Radnor/"
if DEBUG:
    DATA_FOLDER = "data/local/"

CLUB_FILE = "/club.json"
FIXTURES_FILE = "/fixtures.json"
PLAYER_FILE = "/players.json"
MATCH_REPORTS_FILE = "/match_reports.json"
TRAINING_REPORTS_FILE = "/training_reports.json"
TRAINING_VENUES_FILE = "/training_venues.json"

def save_club(club, folder=None):
    if folder == None:
        folder = DATA_FOLDER + club.name
    else:
        folder = folder + club.name
        
    if not os.path.exists(folder):
        os.mkdir(folder)
    save_object_to_json(folder + CLUB_FILE, club)
    save_to_json(folder + PLAYER_FILE, club.players)
    save_to_json(folder + FIXTURES_FILE, club.fixtures)
    save_to_json(folder + MATCH_REPORTS_FILE, club.match_reports)
    save_to_json(folder + TRAINING_VENUES_FILE, club.training_venues)
    save_to_json(folder + TRAINING_REPORTS_FILE, club.training_reports)

def load_club(club, folder=None):
    if folder == None:
        folder = DATA_FOLDER + club.name
    else:
        folder = folder + club.name

    load_object_from_json(folder + CLUB_FILE, club)
    load_from_json(folder + PLAYER_FILE, Player, club.players)
    load_from_json(folder + FIXTURES_FILE, Fixture, club.fixtures)
    load_from_json(folder + MATCH_REPORTS_FILE, MatchReport, club.match_reports)
    load_from_json(folder + TRAINING_VENUES_FILE, TrainingVenue, club.training_venues)
    load_from_json(folder + TRAINING_REPORTS_FILE, TrainingReport, club.training_reports)