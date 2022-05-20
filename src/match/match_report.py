import json

MAX_PLAYERS = 11
MAX_SUBS = 5

# A match report tracks all the data that we know occurred for a given match
class MatchReport:

    def __init__(self):
        self.starting_lineup = []
        self.subs = []

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
        
    def FromJson(self, json_data):
        self.starting_lineup = json_data["starters"]
        self.subs = json_data["subs"]

    def ToJson(self):
        return {
            "starters" : self.starting_lineup,
            "subs": self.subs
        }