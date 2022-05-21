from enum import Enum

MAX_PLAYERS = 11
MAX_SUBS = 5

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

# A match report tracks all the data that we know occurred for a given match
class MatchReport:

    def __init__(self):
        self.starting_lineup = []
        self.subs = []
        self.match_type = MatchType.LEAGUE
        self.venue = Venue.HOME

    def AddStarter(self, player):
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player.name)
    
    def AddSub(self, player):
        if len(self.subs) >= MAX_SUBS:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player.name)

    def RemoveStarter(self, player):
        self.starting_lineup.remove(player.name)

    def RemoveSub(self, player):
        self.subs.remove(player.name)
    
    def GetMatchType(self):
        return self.match_type.name

    def GetVenue(self):
        return self.venue.name

    def FromJson(self, json_data):
        self.starting_lineup = json_data["starters"]
        self.subs = json_data["subs"]
        self.match_type = MatchType(json_data["match_type"])
        self.venue = Venue(json_data["venue"])

    def ToJson(self):
        return {
            "starters" : self.starting_lineup,
            "subs": self.subs,
            "match_type": self.match_type.value,
            "venue": self.venue.value
        }