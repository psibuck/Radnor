from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import GetDateString, JsonGet

# A trainig report tracks who attended a training session on which date etc
class TrainingReport:

    def __init__(self):
        self.attendees = []
        self.venue = None
        self.date = ""

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

    def ToJson(self):
        return {
            "attendees": self.attendees,
            "venue": self.venue.ToJson(),
            "date": self.date
        }
    
    def FromJson(self, json_data):
        self.attendees = json_data["attendees"]
        self.venue = TrainingVenue()
        self.venue.FromJson(json_data["venue"])
        self.date = JsonGet(json_data, "date")

    def GetDate(self):
        return GetDateString(self.date)
        
        