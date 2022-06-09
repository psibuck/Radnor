from src.utilities.data_utilities import json_get

class Club:

    def __init__(self, name, update_callback=None):
        self.name = name
        self.update_callback = update_callback

        self.clear_club_data()

    def clear_club_data(self):
        # Before these were explicit to avoid adding incorrect objects
        # investigate why this fails in load from json
        self.players = []
        self.match_reports = []
        self.training_reports = []
        self.training_venues = [] 
        self.fixtures = []
        self.opponents = []

    def setup_club(self):
        self.process_match_reports()
        self.process_training_reports()

    def add_player(self, new_player):
        for player in self.players:
            if player.get_name() == new_player.get_name():
                return False, "Player must have distinct name"
        self.players.append(new_player)
        self.players.sort()
        if self.update_callback != None:
            self.update_callback()
        return True, None
    
    def update_player(self, old_player, new_player):
        if old_player not in self.players:
            return False, "ERROR: attempting to edit a player who doesn't exist"
        
        old_player_index = self.players.index(old_player)
        self.players[old_player_index] = new_player
        self.players.sort()
        return True, ""

    def add_match_report(self, report):
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

    def add_training_report(self, report):
        self.training_reports.append(report)
        self.process_training_report(report)
        self.training_reports.sort()
        self.update_callback()

    def remove_player(self, player):
        self.players.remove(player)
        self.players.sort()
        return True, ""

    def remove_match_report(self, report):
        self.match_reports.remove(report)
        self.process_match_report(report, False)

    def process_match_reports(self):
        for report in self.match_reports:
            self.process_match_report(report)
    
    def process_match_report(self, report, add=True):
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

    def process_training_report(self, report):
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