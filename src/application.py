"""The application module is concerned with starting the program and the core modules e.g UI/DATABASE"""

import os
import shutil
from typing import Callable, Union

from src.club.club import Club
from src.club.club_creation import ClubCreationData
from src.utilities.save_utilities import DATA_FOLDER, save_club, load_club


class Application:
    """The core application class which controls the lifetime of the app."""

    def __init__(self, debug=False):
        self.is_debug = debug
        self.club: Club = None
        self.clubs: list[ClubCreationData] = []
        self.on_club_loaded: Union[None, Callable] = None
        self.on_application_shutdown: Union[None, Callable] = None

        self._populate_clubs()
        self._make_data_structure()

        self.is_running = True

    def _get_data_folder(self) -> str:
        if self.is_debug:
            return "data/local/"
        return DATA_FOLDER

    def _populate_clubs(self) -> None:
        self.clubs: list[ClubCreationData] = []

        data_folder: str = self._get_data_folder()
        if os.path.exists(data_folder):
            for _, dirs, _ in os.walk(data_folder):
                for dir_name in dirs:
                    self.clubs.append(ClubCreationData(dir_name, ""))

    def _make_data_structure(self) -> None:
        """Construct the data structure that we save data to."""
        path_string = ""
        components = self._get_data_folder().split("/")
        for component in components:
            path_string += component
            if not os.path.exists(path_string):
                os.mkdir(path_string)
            path_string += "/"

    def add_club(self, club_data: ClubCreationData) -> None:
        """Function to add a new club object. Should probably be in the database layer."""
        os.mkdir(self._get_data_folder() + club_data.name)
        self.clubs.append(club_data)
        self.clubs.sort()

    def edit_club(self, new_club_data: ClubCreationData) -> None:
        """This function takes some new club data and overwrites the stored club data"""
        self._delete_club(new_club_data.name)
        self.add_club(new_club_data)

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

    def select_club(self, club: ClubCreationData):
        """Function to select and load a different club to the one currently loaded."""
        self.club = Club(club, self.handle_club_data_changed)
        if self.is_debug:
            load_club(self.club, "data/local/")
        else:
            load_club(self.club)
        self.club.setup_club()
        if self.on_club_loaded is not None:
            self.on_club_loaded(self.club)

    def remove_club(self, club: Club):
        """Delete a club from the application."""
        self._delete_club(club.name)
        self._populate_clubs()

    def _delete_club(self, club_name: str):
        path = "data/local/" + club_name if self.is_debug else DATA_FOLDER + club_name
        if os.path.exists(path):
            shutil.rmtree(path)
