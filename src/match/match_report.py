MAX_PLAYERS = 11
MAX_SUBS = 5

# A match report tracks all the data that we know occurred for a given match
class MatchReport:

    def __init__(self):
        self.date = ""
        self.match_type = ""
        self.home_team = ""
        self.away_team = ""
        self.starting_lineup = []
        self.subs = []
        self.goalscorers = []
        self.assists = []
        self.motm = ""
        self.kit = ""

    def AddStarter(self,player_name):
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player_name)
    
    def AddSub(self,player_name):
        if len(self.subs) >= MAX_SUBS:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player_name)
        
    def LoadFromFile(self, match_report_file):
        return
        
    def SaveToFile(self):
        return
