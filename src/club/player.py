from datetime import date
from src.utilities.data_utilities import json_get

class Player:

    def __init__(self, first_name="", surname=""):
        self.dob = date.today()
        self.is_signed_on = False

        self.matches_started = 0
        self.matches_as_sub = 0

        self.training_attendance = 0

    def __lt__(self, other):
        return self.get_name().lower() < other.get_name().lower()

    def __str__(self) -> str:
        return self.get_name()

    def get_name(self):
        return self.first_name + " " + self.surname

    def from_json(self, json_data):
        self.first_name = json_get(json_data, "first_name")
        self.surname = json_get(json_data, "surname")
        self.dob = json_get(json_data, "dob", type=date)
        return
    
    def to_json(self):
        return {
            "first_name": self.first_name,
            "surname": self.surname,
            "dob": self.dob.isoformat(),
        }

    def get_appearances(self):
        return str(self.matches_started) + "(" + str(self.matches_as_sub) + ")"