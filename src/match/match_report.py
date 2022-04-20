MAX_PLAYERS = 11
MAX_SUBS = 5

# A match report tracks all the data that we know occurred for a given match
class MatchReport:

    def __init__(self):
        self.starting_lineup = []
        self.subs = []

    def AddStarter(self, player_name):
        if len(self.starting_lineup) >= MAX_PLAYERS:
            print("ERROR: Starting lineup is full")
        else:
            self.starting_lineup.append(player_name)
    
    def AddSub(self,player_name):
        if len(self.subs) >= MAX_SUBS:
            print("ERROR: Subs bench is full")
        else:
            self.subs.append(player_name)

    def RemoveStarter(self, player_name):
        self.starting_lineup.remove(player_name)

    def RemoveSub(self, player_name):
        self.subs.remove(player_name)
        
    def GenListString(self, list):
        string_out = "["
        initial = True
        for entry in list:
            if not initial:
                string_out += ","
            else:
                initial = False
            
            string_out += entry
        string_out += "]"
        return string_out

    # TO-DO Make this JSON
    def Save(self, file):
        starters = self.GenListString(self.starting_lineup)
        subs = self.GenListString(self.subs)
        file.write(starters + ";" + subs)

    # TO-DO Make this Json
    def Load(self, file_data):
        data = file_data.split(";")
        self.starting_lineup = data[0].strip("[").strip("]").split(",")
        self.subs = data[1].strip("[").strip("]").split(",")