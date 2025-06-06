"""This file contains the Player class and all related helpers."""

from datetime import date
import src.database.json_utilities as JsonUtil


class Player:
    """The player class which contains data and functions all related to the players who play for the team."""

    def __init__(self, first_name="", surname=""):
        self.first_name: str = first_name
        self.surname: str = surname
        self.dob: date = date.today()
        self.is_signed_on: bool = False

        self.matches_started: int = 0
        self.matches_as_sub: int = 0

        self.training_attendance: int = 0

        self.goals: int = 0
        self.assists: int = 0

        # A list of identifiers used for this player, for example in bank transactions
        self.aliases: list[str] = []

    def __eq__(self, other_player: "Player") -> bool:
        if other_player is None:
            return False
        return (
            self.first_name == other_player.first_name
            and self.surname == other_player.surname
            and self.dob == other_player.dob
        )

    def __lt__(self, other: "Player") -> bool:
        return self.get_name().lower() < other.get_name().lower()

    def __str__(self) -> str:
        return self.get_name()

    def get_name(self) -> str:
        return self.first_name + " " + self.surname

    def get_is_signed_on(self) -> str:
        if self.is_signed_on:
            return "YES"
        return "NO"

    def from_json(self, json_data):
        self.first_name = JsonUtil.get(json_data, "first_name")
        self.surname = JsonUtil.get(json_data, "surname")
        self.dob = JsonUtil.get(json_data, "dob", type=date)
        is_signed_on = JsonUtil.get(json_data, "signed_on")
        if is_signed_on == "YES":
            self.is_signed_on = True

    def to_json(self):
        return {
            "first_name": self.first_name,
            "surname": self.surname,
            "dob": self.dob.isoformat(),
            "signed_on": self.get_is_signed_on(),
        }

    def get_appearances(self) -> str:
        return str(self.matches_started) + "(" + str(self.matches_as_sub) + ")"
