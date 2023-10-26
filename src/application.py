"""The application module is concerned with starting the program and the core modules e.g UI/DATABASE"""
import os
import shutil
from typing import Callable, Union


from src.Club.club import *
from src.utilities.save_utilities import DATA_FOLDER, save_club, load_club


class Application:
    """The core application class which controls the lifetime of the app."""

    def __init__(self, debug=False):
        self.is_debug = debug
        self.club: Club.Club = None
        self.clubs: list[Club.ClubCreationData] = []
        self.on_club_loaded: Union[None, Callable] = None
        self.on_application_shutdown:  Union[None, Callable] = None

        self._populate_clubs()
        self._make_data_structure()

        self.is_running = True

    def _get_data_folder(self) -> str:
        if self.is_debug:
            return "data/local/"
        return DATA_FOLDER

    def _populate_clubs(self) -> None:
        data_folder: str = self._get_data_folder()
        if os.path.exists(data_folder):
            for _, dirs, _ in os.walk(data_folder):
                for dir_name in dirs:
                    self.clubs.append(Club.ClubCreationData(dir_name, ""))

    def _make_data_structure(self) -> None:
        """Construct the data structure that we save data to."""
        path_string = ""
        components = self._get_data_folder().split("/")
        for component in components:
            path_string += component
            if not os.path.exists(path_string):
                os.mkdir(path_string)
            path_string += "/"

    def add_club(self, club_data: Club.ClubCreationData) -> None:
        """Function to add a new club object. Should probably be in the database layer."""
        print("ADD CLUB")
        print(club_data)
        os.mkdir(self._get_data_folder() + club_data.name)
        self.clubs.append(club_data.name)
        # self.clubs.sort()

    def clear_local_data(self):
        """Deletes all local data"""
        if os.path.exists(DATA_FOLDER):
            shutil.rmtree(DATA_FOLDER)

        self.club.clear_club_data()

    def handle_club_data_changed(self):
        """Interface for saving the club down locally."""
        if self.is_debug:
            save_club(self.club, "data/local/")
        else:
            save_club(self.club)

    def quit(self):
        """The quit function for the entire application."""
        if self.club is not None:
            if self.is_debug:
                save_club(self.club, "data/local/")
            else:
                save_club(self.club)
        if self.on_application_shutdown is not None:
            self.on_application_shutdown()

    def select_club(self, club: Club.ClubCreationData):
        """Function to select and load a different club to the one currently loaded."""
        self.club = Club.Club(club, self.handle_club_data_changed)
        if self.is_debug:
            load_club(self.club, "data/local/")
        else:
            load_club(self.club)
        self.club.setup_club()
        if self.on_club_loaded is not None:
            self.on_club_loaded(self.club)

    def remove_club(self, club_name: str = ""):
        """Delete a club from the database."""
        if club_name == "":
            club_name = self.club.name
        self._delete_club(club_name)
        self._populate_clubs()
        return

    def _delete_club(self, club: Club.Club):
        path = DATA_FOLDER + club.name
        if os.path.exists(path):
            shutil.rmtree(path)
