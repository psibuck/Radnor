from ui.page_manager import PageManager

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

while app.is_running:
    PM.Draw()
    
