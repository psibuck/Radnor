import os
import shutil

from src.club.club import Club
from src.utilities.save_utilities import save_club, load_club
from ui.page_manager import PageManager

CLUB_DATA_PATH = "data/local/"

class Application:

    def __init__(self):
        self.make_data_structure()
        self.populate_clubs()
        self.club = None
        self.ui = PageManager(self)
        
        self.is_running = True

    def populate_clubs(self):
        self.clubs = []
        if os.path.exists(CLUB_DATA_PATH):
            for _, dirs, _ in os.walk(CLUB_DATA_PATH):
                for dir in dirs:
                    self.clubs.append(dir)

    def add_club(self, club_name):
        os.mkdir(CLUB_DATA_PATH + club_name)
        self.clubs.append(club_name)
        self.clubs.sort()

    def make_data_structure(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(CLUB_DATA_PATH):
            os.mkdir(CLUB_DATA_PATH)   

    def activate(self):
        self.ui.draw()

    def clear_local_data(self):
        if os.path.exists(CLUB_DATA_PATH + self.club.name):
            shutil.rmtree(CLUB_DATA_PATH + self.club.name)
    
        self.club.clear_club_data()

    def handle_club_data_changed(self):
        save_club(self.club)

    def quit(self):
        save_club(self.club)
        self.ui.shutdown()

    def select_club(self, club):
        self.club = Club(club, self.handle_club_data_changed)
        load_club(self.club)
        self.ui.handle_club_loaded()

# Refactor this, consider role of page manager vs app, same thing?
app = Application()
app.activate()