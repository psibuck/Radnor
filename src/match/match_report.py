from src.match.fixture import Fixture, MatchType, Venue
from src.match.goal import Goal
from src.utilities.data_utilities import json_get

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
        self.goals = []

    def from_fixture(self, fixture):
        self.date = fixture.date
        self.opponent = fixture.opponent
        self.venue = fixture.venue
        self.match_type = fixture.match_type

    def add_starter(self, player):
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player.get_name())
    
    def add_sub(self, player):
        if len(self.subs) >= MAX_SUBS and self.match_type != MatchType.FRIENDLY:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player.get_name())

    def add_goal(self, goal):
        self.goals.append(goal)

    def remove_starter(self, player):
        self.starting_lineup.remove(player.get_name())

    def remove_sub(self, player):
        self.subs.remove(player.get_name())
    
    def get_scoreline(self):
        if self.venue == Venue.AWAY:
            return self.opponent + str(self.opponent_goals) + "-" + str(self.club_goals) + " " + "test"
        else:
            return "test" + " " + str(self.club_goals) + "-" + str(self.opponent_goals) + " " + self.opponent
        
    def from_json(self, json_data):
        self.starting_lineup = json_get(json_data, "starters")
        self.subs = json_get(json_data, "subs")
        self.club_goals = json_get(json_data, "num_goals", type=int)
        self.opponent_goals = json_get(json_data, "opponent_goals", type=int)
        super().from_json(json_data["fixture"])

        goals_raw = json_get(json_data, "goals")
        for goal in goals_raw:
            new_goal = Goal()
            new_goal.from_json(goal)
            self.goals.append(new_goal)

    def to_json(self):
        goals_json = []
        for goal in self.goals:
            goals_json.append(goal.to_json())

        return {
            "starters" : self.starting_lineup,
            "subs": self.subs,
            "num_goals": self.club_goals,
            "opponent_goals": self.opponent_goals,
            "fixture": super().to_json(),
            "goals": goals_json
        }