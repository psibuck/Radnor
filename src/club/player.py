

class Player:

    def __init__(self, name=""):
        self.name = name
        self.is_signed_on = False

        self.matches_started = 0
        self.matches_as_sub = 0

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    # TO-DO Make this JSON
    def Save(self, file):
        file.write(self.name + "\n")
        return

    # TO-DO Make this Json
    def Load(self, file_data):
        self.name = file_data[0]
        return

    def GetAppearances(self):
        return str(self.matches_started) + "(" + str(self.matches_as_sub) + ")"

