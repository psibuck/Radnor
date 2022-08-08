from difflib import Match
from src.finances.financial_utilities import *
from src.finances.transaction import *
from src.utilities.data_utilities import json_get

import src.club.player as Player
import src.club.training_report as TrainingReport
import src.match.match_report as MatchReport

class Club:

    def __init__(self, name, update_callback=None):
        self.name = name
        self.update_callback = update_callback

        self.clear_club_data()

    def clear_club_data(self):
        # Before these were explicit to avoid adding incorrect objects
        # investigate why this fails in load from json
        self.players: list[Player.Player] = []
        self.match_reports: list[MatchReport.MatchReport] = []
        self.training_reports: list[TrainingReport.TrainingReport] = []
        self.training_venues = [] 
        self.fixtures = []
        self.opponents = []

    def setup_club(self):
        self.process_match_reports()
        self.process_training_reports()

    def add_player(self, new_player: Player.Player):
        for player in self.players:
            if player.get_name() == new_player.get_name():
                return False, "Player must have distinct name"
        self.players.append(new_player)
        self.players.sort()
        if self.update_callback != None:
            self.update_callback()
        return True, None
    
    def update_player(self, old_player: Player.Player, new_player: Player.Player):
        if old_player not in self.players:
            return False, "ERROR: attempting to edit a player who doesn't exist"
        
        old_player_index = self.players.index(old_player)
        self.players[old_player_index] = new_player
        self.players.sort()
        return True, ""

    def add_match_report(self, report: MatchReport.MatchReport):
        self.match_reports.append(report)
        self.process_match_report(report)
        self.match_reports.sort()
        if self.update_callback != None:
            self.update_callback()

    def add_fixture(self, fixture):
        self.fixtures.append(fixture)
        self.fixtures.sort()
        self.update_callback()

    def remove_fixture(self, fixture):
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

    def remove_match_report(self, report: MatchReport.MatchReport):
        self.match_reports.remove(report)
        self.process_match_report(report, False)

    def process_match_reports(self):
        for report in self.match_reports:
            self.process_match_report(report)
    
    def process_match_report(self, report: MatchReport.MatchReport, add=True):
        increment = 1
        if not add:
            increment = -1

        for starter in report.starting_lineup:
            player = self.get_player_by_name(starter)
            if player != None:
                player.matches_started += increment

        for sub in report.subs:
            player = self.get_player_by_name(sub)
            if player != None:
                player.matches_as_sub += increment

        for goal in report.goals:
            scorer = self.get_player_by_name(goal.scorer)
            if scorer != None:
                scorer.goals += increment
            assister = self.get_player_by_name(goal.assister)
            if assister != None:
                assister.assists += increment

    def get_player_by_name(self, name):
        for player in self.players:
            if player.get_name() == name:
                return player

    def process_training_report(self, report: TrainingReport.TrainingReport):
        for attendee in report.attendees:
            player = self.get_player_by_name(attendee)
            if player != None:
                player.training_attendance += 1

    def process_training_reports(self):
        for report in self.training_reports:
            self.process_training_report(report)

    def add_opponent(self, opponent):
        self.opponents.append(opponent)
        self.opponents.sort()
        self.update_callback()
    
    def from_json(self, json_data):
        self.name = json_get(json_data, "name")
        self.opponents = json_get(json_data, "opponents")

    def to_json(self):
        return {
            "name": self.name,
            "opponents": self.opponents
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
        for match in self.match_reports:
            if player.get_name() in match.starting_lineup:
                transactions.append(Transaction(match.date, TransactionType.MATCH, amount=get_match_fee(match, MatchRole.STARTER)))
            elif player.get_name() in match.subs:
                transactions.append(Transaction(match.date, TransactionType.MATCH, amount=get_match_fee(match, MatchRole.SUB)))

        for training_session in self.training_reports:
            transactions.append(Transaction(training_session.date, TransactionType.TRAINING, training_session.venue.cost))
            
        return transactions