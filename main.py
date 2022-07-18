import os
import shutil
import sys

from src.club.club import Club
from src.utilities.save_utilities import DATA_FOLDER, save_club, load_club
from ui.page_manager import PageManager

class Application:

    def __init__(self, debug=False):
        self.is_debug = debug
        self.make_data_structure()
        self.populate_clubs()
        self.club = None
        self.ui = PageManager(self)
        
        self.is_running = True

    def get_data_folder(self):
        if self.is_debug:
            return "data/local/"
        return DATA_FOLDER

    def populate_clubs(self):
        self.clubs = []
        if os.path.exists(self.get_data_folder()):
            for _, dirs, _ in os.walk(self.get_data_folder()):
                for dir in dirs:
                    self.clubs.append(dir)

    def add_club(self, club_name):
        os.mkdir(self.get_data_folder() + club_name)
        self.clubs.append(club_name)
        self.clubs.sort()

    def make_data_structure(self):
        path_string = ""
        components = self.get_data_folder().split("/")
        for component in components:
            path_string += component
            if not os.path.exists(path_string):
                os.mkdir(path_string) 
            path_string += "/"

    def activate(self):
        self.ui.draw()

    def clear_local_data(self):
        if os.path.exists(DATA_FOLDER):
            shutil.rmtree(DATA_FOLDER)
    
        self.club.clear_club_data()

    def handle_club_data_changed(self):
        if self.is_debug:
            save_club(self.club, "data/local/")
        else:
            save_club(self.club)

    def quit(self):
        if self.club != None:
            if self.is_debug:
                save_club(self.club, "data/local/")
            else:
                save_club(self.club)
        self.ui.shutdown()

    def select_club(self, club):
        self.club = Club(club, self.handle_club_data_changed)
        if self.is_debug:
            load_club(self.club, "data/local/")
        else:
            load_club(self.club)
        self.ui.handle_club_loaded()

    def remove_club(self, club_name=""):
        if club_name == "":
            club_name = self.club.name
        self._delete_club(club_name)
        self.populate_clubs()
        return

    def _delete_club(self, club):
        path = DATA_FOLDER + self.club.name
        if os.path.exists(path):
            shutil.rmtree(path)

is_debug = "debug" in sys.argv

# Refactor this, consider role of page manager vs app, same thing?
app = Application(is_debug)
app.activate()