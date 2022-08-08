from enum import Enum
import src.match.fixture as Fixture
import src.match.goal as Goal
import src.club.player as Player
from src.utilities.data_utilities import json_get

class MatchRole(Enum):
    STARTER = 1
    SUB = 2
    UNUSED_SUB = 3 

MAX_PLAYERS = 11
MAX_SUBS = 5

# A match report tracks all the data that we know occurred for a given match
class MatchReport(Fixture):

    def __init__(self):
        Fixture.__init__(self)
        self.starting_lineup: list[str] = []
        self.subs: list[str] = []
        self.club_goals = 0
        self.opponent_goals = 0
        self.goals: list[Goal.Goal] = []

    def from_fixture(self, fixture: Fixture.Fixture):
        self.date = fixture.date
        self.opponent = fixture.opponent
        self.venue = fixture.venue
        self.match_type = fixture.match_type

    def add_starter(self, player: Player.Player):
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player.get_name())
    
    def add_sub(self, player: Player.Player):
        if len(self.subs) >= MAX_SUBS and self.match_type != Fixture.MatchType.FRIENDLY:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player.get_name())

    def add_goal(self, goal):
        self.goals.append(goal)

    def remove_starter(self, player: Player.Player):
        self.starting_lineup.remove(player.get_name())

    def remove_sub(self, player: Player.Player):
        self.subs.remove(player.get_name())
    
    def get_scoreline(self):
        if self.venue == Fixture.Venue.AWAY:
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