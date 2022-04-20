from src.club.club import Club
from ui.page_manager import PageManager

from data.file_names import PLAYER_FILE

class Application:

    def __init__(self):
        self.club = Club("Radnor")
        self.club.Load("data/local/" + self.club.name)
        self.ui = PageManager(self)
        
        self.is_running = True

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




    
