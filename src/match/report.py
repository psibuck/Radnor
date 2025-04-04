"""File that contains the MatchReport class and supporting data types."""

from enum import Enum
import src.match.fixture as Fixture
import src.match.goal as Goal
import src.club.player as Player

import src.database.json_utilities as JsonUtil


class MatchRole(Enum):
    """Enum representing the different roles a player can occupy within a match report."""

    STARTER = 1
    SUB = 2
    UNUSED_SUB = 3


MAX_PLAYERS = 11
MAX_SUBS = 5


class MatchReport(Fixture.Fixture):
    """A match report tracks all the data that we know occurred for a played match"""

    def __init__(self):
        Fixture.Fixture.__init__(self)
        self.starting_lineup: list[str] = []
        self.subs: list[str] = []
        self.club_goals: int = 0
        self.opponent_goals: int = 0
        self.goals: list[Goal.Goal] = []
        self.club_name: str = ""

    def from_fixture(self, fixture: Fixture.Fixture):
        """Constructs a match report from a given fixture."""
        self.date = fixture.date
        self.opponent = fixture.opponent
        self.venue = fixture.venue
        self.match_type = fixture.match_type

    def add_starter(self, player: Player.Player):
        """Attempts to move a player into the starting XI."""
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player.get_name())

    def add_sub(self, player: Player.Player):
        """Attempts to move a player onto the subs list."""
        if len(self.subs) >= MAX_SUBS and self.match_type != Fixture.MatchType.FRIENDLY:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player.get_name())

    def add_goal(self, goal):
        """Adds a new goal object to the list of stored goals."""
        self.goals.append(goal)

    def remove_starter(self, player: Player.Player):
        """Attempts to remove a player from the starting XI."""
        self.starting_lineup.remove(player.get_name())

    def remove_sub(self, player: Player.Player):
        """Attempts to remove a player from the subs list."""
        self.subs.remove(player.get_name())

    def get_scoreline(self) -> str:
        """Constructs a string representation of the scoreline."""
        scoreline: str = "{} {} - {} {}"
        if self.venue == Fixture.Venue.AWAY:
            return scoreline.format(
                self.opponent, self.opponent_goals, self.club_goals, self.club_name
            )
        return scoreline.format(
            self.club_name, self.club_goals, self.opponent_goals, self.opponent
        )

    def from_json(self, json_data):
        self.starting_lineup = JsonUtil.get(json_data, "starters")
        self.subs = JsonUtil.get(json_data, "subs")
        self.club_goals = JsonUtil.get(json_data, "num_goals", type=int)
        self.opponent_goals = JsonUtil.get(json_data, "opponent_goals", type=int)
        self.club_name = JsonUtil.get(json_data, "club_name", type=str)
        super().from_json(json_data["fixture"])

        goals_raw = JsonUtil.get(json_data, "goals")
        for goal in goals_raw:
            new_goal = Goal.Goal()
            new_goal.from_json(goal)
            self.goals.append(new_goal)

    def to_json(self):
        goals_json = []
        for goal in self.goals:
            goals_json.append(goal.to_json())

        return {
            "starters": self.starting_lineup,
            "subs": self.subs,
            "num_goals": self.club_goals,
            "opponent_goals": self.opponent_goals,
            "fixture": super().to_json(),
            "goals": goals_json,
            "club_name": self.club_name,
        }
