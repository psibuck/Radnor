from datetime import date
from src.utilities.data_utilities import json_get

class Player:

    def __init__(self, first_name="", surname=""):
        self.first_name = first_name
        self.surname = surname
        self.dob = date.today()
        self.is_signed_on = False

        self.matches_started = 0
        self.matches_as_sub = 0

        self.training_attendance = 0

        self.goals = 0
        self.assists = 0
        
    def __eq__(self, o: object) -> bool:
        if o == None:
            return False
        return self.first_name == o.first_name and self.surname == o.surname and self.dob == o.dob
        
    def __lt__(self, other):
        return self.get_name().lower() < other.get_name().lower()

    def __str__(self) -> str:
        return self.get_name()

    def get_name(self):
        return self.first_name + " " + self.surname

    def get_is_signed_on(self):
        if self.is_signed_on:
            return "YES"
        return "NO"

    def from_json(self, json_data):
        self.first_name = json_get(json_data, "first_name")
        self.surname = json_get(json_data, "surname")
        self.dob = json_get(json_data, "dob", type=date)
        is_signed_on = json_get(json_data, "signed_on")
        if is_signed_on == "YES":
            self.is_signed_on = True
        return
    
    def to_json(self):
        return {
            "first_name": self.first_name,
            "surname": self.surname,
            "dob": self.dob.isoformat(),
            "signed_on": self.get_is_signed_on()
        }

    def get_appearances(self):
        return str(self.matches_started) + "(" + str(self.matches_as_sub) + ")"