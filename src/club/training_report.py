from datetime import date

from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import json_get

# A trainig report tracks who attended a training session on which date etc
class TrainingReport:

    def __init__(self):
        self.attendees = []
        self.venue = None
        self.date = None

    def __eq__(self, other):
        if len(self.attendees) != len(other.attendees):
            return False
        
        i = 0
        while i < len(self.attendees):
            if self.attendees[i] != other.attendees[i]:
                return False
            i += 1
        if self.venue != other.venue:
            return False

        return True

    def GetNumAttendees(self):
        return len(self.attendees)

    def to_json(self):
        return {
            "attendees": self.attendees,
            "venue": self.venue.to_json(),
            "date": self.date.isoformat()
        }
    
    def from_json(self, json_data):
        self.attendees = json_data["attendees"]
        self.venue = TrainingVenue()
        self.venue.from_json(json_data["venue"])
        self.date = date.fromisoformat(json_get(json_data, "date"))

    def get_date(self):
        if self.date != None:
            return self.date.isoformat()
        return "No date set"
        