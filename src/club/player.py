from datetime import date
from src.utilities.data_utilities import json_get

class Player:

    def __init__(self, name=""):
        self.name = name
        self.dob = date.today()
        self.is_signed_on = False

        self.matches_started = 0
        self.matches_as_sub = 0

        self.training_attendance = 0

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    def __str__(self) -> str:
        return self.name

    def from_json(self, json_data):
        self.name = json_get(json_data, "name")
        self.dob = json_get(json_data, "dob", type=date)
        return
    
    def to_json(self):
        return {
            "name": self.name,
            "dob": self.dob.isoformat()
        }

    def get_appearances(self):
        return str(self.matches_started) + "(" + str(self.matches_as_sub) + ")"