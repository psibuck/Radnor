from enum import Enum
from src.utilities.data_utilities import json_get

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
        self.date = ""
        self.opponent = ""
        self.venue = Venue.HOME
        self.match_type = MatchType.LEAGUE

    def from_json(self, json_data):
        self.match_type = json_get(json_data, "match_type", MatchType)
        self.venue = json_get(json_data, "venue", Venue)
        self.opponent = json_get(json_data, "opponent")
        self.date = json_get(json_data, "date")

    def to_json(self):
        return {
            "match_type": self.match_type.value,
            "venue": self.venue.value,
            "opponent": self.opponent,
            "date": self.date
        }