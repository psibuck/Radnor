from src.club.club_creation import ClubCreationData
from src.finances.financial_utilities import get_match_fee, MatchRole
from src.finances.transaction import Transaction, TransactionType

import src.club.player as Player
import src.training.report as TrainingReport
import src.training.venue as TrainingVenue
import src.match.fixture as Fixture
import src.match.report as MatchReport
import src.finances.transaction_manager as TransactionManager

import src.database.json_utilities as JsonUtil
from typing import Callable


class Club:

    def __init__(self, club_data: ClubCreationData, update_callback: Callable = None):
        self.name: str = club_data.name
        self.short_name: str = club_data.short_name
        self.update_callback = update_callback

        self.players: list[Player.Player] = []
        self.match_reports: list[MatchReport.MatchReport] = []
        self.training_reports: list[TrainingReport.TrainingReport] = []
        self.training_venues: list[TrainingVenue.TrainingVenue] = []
        self.fixtures: list[Fixture.Fixture] = []
        self.opponents: list[str] = []

    def __lt__(self, other_club: "Club") -> bool:
        return self.name > other_club.name

    def clear_club_data(self) -> None:
        self.players: list[Player.Player] = []
        self.match_reports: list[MatchReport.MatchReport] = []
        self.training_reports: list[TrainingReport.TrainingReport] = []
        self.training_venues: list[TrainingVenue.TrainingVenue] = []
        self.fixtures: list[Fixture.Fixture] = []
        self.opponents: list[str] = []

    def setup_club(self):
        from src.processors.match_report_processor import MatchReportProcessor

        MatchReportProcessor.process_match_reports(self)
        self.process_training_reports()

    def add_player(self, new_player: Player.Player):
        for player in self.players:
            if player.get_name() == new_player.get_name():
                return False, "Player must have distinct name"
        self.players.append(new_player)
        self.players.sort()
        if self.update_callback is not None:
            self.update_callback()
        return True, None

    def update_player(self, old_player: Player.Player, new_player: Player.Player):
        if old_player not in self.players:
            return False, "ERROR: attempting to edit a player who doesn't exist"

        old_player_index = self.players.index(old_player)
        self.players[old_player_index] = new_player
        self.players.sort()
        return True, ""

    def add_fixture(self, fixture: Fixture.Fixture):
        self.fixtures.append(fixture)
        self.fixtures.sort()
        self.update_callback()

    def remove_fixture(self, fixture: Fixture.Fixture):
        self.fixtures.remove(fixture)

    def add_training_report(self, report: TrainingReport.TrainingReport):
        self.training_reports.append(report)
        self.process_training_report(report)
        self.training_reports.sort()
        self.update_callback()

    def remove_player(self, player):
        self.players.remove(player)
        self.players.sort()
        return True, ""

    def get_player_by_name(self, name):
        for player in self.players:
            if player.get_name() == name:
                return player

    def process_training_report(self, report: TrainingReport.TrainingReport):
        for attendee in report.attendees:
            player = self.get_player_by_name(attendee)
            if player is not None:
                player.training_attendance += 1

    def process_training_reports(self):
        for report in self.training_reports:
            self.process_training_report(report)

    def add_opponent(self, opponent):
        self.opponents.append(opponent)
        self.opponents.sort()
        self.update_callback()

    def from_json(self, json_data):
        self.name = JsonUtil.get(json_data, "name")
        self.short_name = JsonUtil.get(json_data, "short_name")
        self.opponents = JsonUtil.get(json_data, "opponents")

    def to_json(self):
        return {
            "name": self.name,
            "short_name": self.short_name,
            "opponents": self.opponents,
        }

    def get_top_scorers(self, num):
        players = self.players[:]
        players = sorted(players, key=lambda player: player.goals, reverse=True)
        return players[:num]

    def get_player_names(self):
        players_out = []
        for player in self.players:
            players_out.append(player.get_name())
        return players_out

    def get_player_transaction_list(self, player: Player.Player) -> list[Transaction]:
        transactions: list[Transaction] = []

        player_name = player.get_name()
        for match in self.match_reports:
            if player_name in match.starting_lineup:
                transactions.append(
                    Transaction(
                        player_name,
                        match.date,
                        TransactionType.MATCH,
                        amount=get_match_fee(match, MatchRole.STARTER),
                    )
                )
            elif player_name in match.subs:
                transactions.append(
                    Transaction(
                        player_name,
                        match.date,
                        TransactionType.MATCH,
                        amount=get_match_fee(match, MatchRole.SUB),
                    )
                )

        for training_session in self.training_reports:
            transactions.append(
                Transaction(
                    player_name,
                    training_session.date,
                    TransactionType.TRAINING,
                    training_session.venue.cost,
                )
            )

        return TransactionManager.get_player_transactions(player)
