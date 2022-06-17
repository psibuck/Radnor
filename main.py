import os
import shutil

from src.club.club import Club
from src.utilities.save_utilities import save_club, load_club
from ui.page_manager import PageManager

class Application:

    def __init__(self):
        self.make_data_structure()
        self.populate_clubs()

        self.club = Club("Radnor", self.handle_club_data_changed)
        load_club(self.club)
        self.ui = PageManager(self)
        
        self.is_running = True

    def populate_clubs(self):
        self.clubs = []
        if os.path.exists("data/local"):
            for subdirs, dirs, files in os.walk("data/local"):
                for dir in dirs:
                    self.clubs.append(dir)

    def make_data_structure(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/local"):
            os.mkdir("data/local")   

    def activate(self):
        self.ui.draw()

    def clear_local_data(self):
        if os.path.exists(DATA_FOLDER + self.club.name):
            shutil.rmtree(DATA_FOLDER + self.club.name)
    
        self.club.clear_club_data()

    def handle_club_data_changed(self):
        save_club(self.club)

    def quit(self):
        save_club(self.club)
        self.ui.shutdown()

# Refactor this, consider role of page manager vs app, same thing?
app = Application()
app.activate()