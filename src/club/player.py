

class Player:

    def __init__(self):
        self.name = ""
        self.is_signed_on = False

    # TO-DO Make this JSON
    def Save(self, file):
        file.write(self.name + "\n")
        return

    # TO-DO Make this Json
    def Load(self, file_data):
        self.name = file_data[0]
        return

