"""Contains functions concerned with saving and loading data."""

from typing import Union
import os

from src.club.player import Player
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from src.match.fixture import Fixture
from src.match.match_report import MatchReport

import src.club.club as Club
import src.utilities.data_utilities as DataUtil

DATA_FOLDER = "C:/Users/psibu/Documents/Radnor/"

CLUB_FILE = "/club.json"
FIXTURES_FILE = "/fixtures.json"
PLAYER_FILE = "/players.json"
MATCH_REPORTS_FILE = "/match_reports.json"
TRAINING_REPORTS_FILE = "/training_reports.json"
TRAINING_VENUES_FILE = "/training_venues.json"

def save_club(club: Club.Club, folder: Union[str, None] = None):
    """Saves the given club to the given folder."""
    if folder is None:
        folder = DATA_FOLDER + club.name
    else:
        folder = folder + club.name
        
    if not os.path.exists(folder):
        os.mkdir(folder)
    DataUtil.save_object_to_json(folder + CLUB_FILE, club)
    DataUtil.save_to_json(folder + PLAYER_FILE, club.players)
    DataUtil.save_to_json(folder + FIXTURES_FILE, club.fixtures)
    DataUtil.save_to_json(folder + MATCH_REPORTS_FILE, club.match_reports)
    DataUtil.save_to_json(folder + TRAINING_VENUES_FILE, club.training_venues)
    DataUtil.save_to_json(folder + TRAINING_REPORTS_FILE, club.training_reports)

def load_club(club: Club.Club, folder: Union[str, None] = None):
    """Loads all the club data from the given folder into the given club object."""
    if folder is None:
        folder = DATA_FOLDER + club.name
    else:
        folder = folder + club.name

    DataUtil.load_object_from_json(folder + CLUB_FILE, club)
    DataUtil.load_from_json(folder + PLAYER_FILE, Player, club.players)
    DataUtil.load_from_json(folder + FIXTURES_FILE, Fixture, club.fixtures)
    DataUtil.load_from_json(folder + MATCH_REPORTS_FILE, MatchReport, club.match_reports)
    DataUtil.load_from_json(folder + TRAINING_VENUES_FILE, TrainingVenue, club.training_venues)
    DataUtil.load_from_json(folder + TRAINING_REPORTS_FILE, TrainingReport, club.training_reports)