from datetime import date

from src.training.venue import TrainingVenue
import src.database.json_utilities as JsonUtil

# A trainig report tracks who attended a training session on which date etc


class TrainingReport:

    def __init__(self):
        self.attendees: list[str] = []
        self.venue: TrainingVenue = None
        self.date: date = date.today()

    def __eq__(self, other):
        if other is None:
            return False
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

    def __lt__(self, o):
        return self.date < o.date

    def __gt__(self, o):
        return self.date > o.date

    def to_json(self):
        return {
            "attendees": self.attendees,
            "venue": self.venue.to_json(),
            "date": self.date.isoformat(),
        }

    def from_json(self, json_data):
        self.attendees = json_data["attendees"]
        self.venue = TrainingVenue()
        self.venue.from_json(json_data["venue"])
        self.date = date.fromisoformat(JsonUtil.get(json_data, "date"))

    def get_date(self):
        if self.date is None:
            return self.date.isoformat()
        return "No date set"

    def get_num_attendees(self):
        """Return the number of players that attended training."""
        return len(self.attendees)
