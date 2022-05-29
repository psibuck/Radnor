from src.match.fixture import Fixture, Venue
from src.utilities.data_utilities import JsonGet, GetDateString

MAX_PLAYERS = 11
MAX_SUBS = 5

# A match report tracks all the data that we know occurred for a given match
class MatchReport(Fixture):

    def __init__(self):
        Fixture.__init__(self)
        self.starting_lineup = []
        self.subs = []
        self.club_goals = 0
        self.opponent_goals = 0
    
    def FromFixture(self, fixture):
        self.date = fixture.date
        self.opponent = fixture.opponent
        self.venue = fixture.venue
        self.match_type = fixture.match_type

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
    
    def GetScoreline(self):
        if self.venue == Venue.AWAY:
            return self.opponent + str(self.opponent_goals) + "-" + str(self.club_goals) + " " + "test"
        else:
            return "test" + " " + str(self.club_goals) + "-" + str(self.opponent_goals) + " " + self.opponent

    def GetDate(self):
        return GetDateString(self.date)
        
    def FromJson(self, json_data):
        self.starting_lineup = JsonGet(json_data, "starters")
        self.subs = JsonGet(json_data, "subs")
       # self.match_type = JsonGet(json_data, "match_type", MatchType)
        #self.venue = JsonGet(json_data, "venue", Venue)
        #self.opponent = JsonGet(json_data, "opponent")
        self.club_goals = JsonGet(json_data, "goals", type=int)
        self.opponent_goals = JsonGet(json_data, "opponent_goals", type=int)
        #self.date = JsonGet(json_data, "date")
        super().FromJson(json_data["fixture"])

    def ToJson(self):
        return {
            "starters" : self.starting_lineup,
            "subs": self.subs,
            #"match_type": self.match_type.value,
            #"venue": self.venue.value,
            #"opponent": self.opponent,
            "goals": self.club_goals,
            "opponent_goals": self.opponent_goals,
            #"date": self.date,
            "fixture": super().ToJson()
        }