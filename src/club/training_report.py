from src.club.training_venue import TrainingVenue
from src.utilities.data_utilities import GenerateListString, LoadArray

# A trainig report tracks who attended a training session on which date etc
class TrainingReport:

    def __init__(self):
        self.attendees = []
        self.venue = None

    def Load(self, file):
        data = file.split(";")
        if len(data) != 2:
            print("Error loading training report")
            return
        self.attendees = LoadArray(data[0])        
        self.venue = TrainingVenue()
        self.venue.Load(data[1])

        return

    def Save(self, file):
        if len(self.attendees) == 0:
            print("Tried to save training report but attendees list empty")
            return
        if self.venue is None:
            print("Tried to save training report but no venue set")
            return

        attendees = GenerateListString(self.attendees)
        venue = self.venue.Stringify()
        file.write(attendees + ";" + venue + "\n")

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
        
        