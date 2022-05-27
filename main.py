import os

from src.club.club import Club
from ui.page_manager import PageManager

class Application:

    def __init__(self):
        self.MakeDataStructure()

        self.club = Club("Radnor")
        self.club.Load("data/local/" + self.club.name)
        self.ui = PageManager(self)
        
        self.is_running = True

    def MakeDataStructure(self):
        os.mkdir("data")
        os.mkdir("data/local")

    def Activate(self):
        self.ui.Draw()

    def LoadMatchReports(self):
        return
    
    def Quit(self):
        app.club.SaveClub("data/local/" + app.club.name)
        self.ui.Shutdown()

# Refactor this, consider role of page manager vs app, same thing?
app = Application()
app.Activate()




    
