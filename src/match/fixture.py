from datetime import date
from enum import Enum
import src.utilities.json_utilities as JsonUtil

class MatchType(Enum):
    LEAGUE = 1
    CUP = 2
    FRIENDLY = 3 

    def __str__(self):
        return self.name

class Venue(Enum):
    HOME = 1
    AWAY = 2
    NEUTRAL = 3

    def __str__(self):
        return self.name

# A fixture is a match that has yet to be played
class Fixture:
    def __init__(self):
        self.date = date.today()
        self.opponent = ""
        self.venue = Venue.HOME
        self.match_type = MatchType.LEAGUE

    def __str__(self):
        return self.opponent + "(" + str(self.venue) + ") - " + self.date.isoformat()

    def __lt__(self, o):
        return self.date < o.date
    
    def __gt__(self, o):
        return self.date > o.date

    def from_json(self, json_data):
        self.match_type = JsonUtil.get(json_data, "match_type", MatchType)
        self.venue = JsonUtil.get(json_data, "venue", Venue)
        self.opponent = JsonUtil.get(json_data, "opponent")
        self.date = date.fromisoformat(JsonUtil.get(json_data, "date"))

    def to_json(self):
        return {
            "match_type": self.match_type.value,
            "venue": self.venue.value,
            "opponent": self.opponent,
            "date": self.date.isoformat()
        }
    
    def get_match_type(self):
        return self.match_type.name

    def get_date(self):
        if self.date != None:
            return self.date.isoformat()
        return "No date set"
