from src.utilities.data_utilities import json_get

class Club:

    def __init__(self, name, update_callback):
        self.name = name
        self.update_callback = update_callback

        # Before these were explicit to avoid adding incorrect objects
        # investigate why this fails in load from json
        self.players = []
        self.match_reports = []
        self.training_reports = []
        self.training_venues = []
        self.fixtures = []
        self.opponents = []

    def SetupClub(self):
        self.process_match_reports()
        self.process_training_reports()

    def add_player(self, new_player):
        for player in self.players:
            if player.get_name() == new_player.get_name():
                return False, "Player must have distinct name"
        self.players.append(new_player)
        self.players.sort()
        self.update_callback()
        return True, None
    
    def add_match_report(self, report):
        self.match_reports.append(report)
        self.process_match_report(report)
        self.match_reports.sort()
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

    def remove_match_report(self, report):
        self.match_reports.remove(report)
        self.process_match_report(report, False)

    def process_match_reports(self):
        for report in self.match_reports:
            self.process_match_report(report)
    
    def process_match_report(self, report, add=True):
        for starter in report.starting_lineup:
            for player in self.players:
                if player.name == starter:
                    if add:
                        player.matches_started += 1
                    else:
                        player.matches_started -= 1
        for sub in report.subs:
            for player in self.players:
                if player.name == sub:
                    if add:
                        player.matches_as_sub += 1
                    else:
                        player.matches_as_sub -= 1

    def process_training_report(self, report):
        for attendee in report.attendees:
            for player in self.players:
                if player.name == attendee:
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

        