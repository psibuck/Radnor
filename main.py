from src.club.club import Club
from ui.page_manager import PageManager

from data.file_names import PLAYER_FILE

class Application:

    def __init__(self):
        self.players = self.LoadPlayers()
        self.is_running = True

    def LoadPlayers(self):
        return

    def LoadMatchReports(self):
        return
    
    def Quit(self):
        self.is_running = False


app = Application()
PM = PageManager()
club = Club()
club.LoadPlayers(PLAYER_FILE)

while app.is_running:
    PM.Draw()

club.SaveClub(PLAYER_FILE)


    
