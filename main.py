import os

from src.club.club import Club
from ui.page_manager import PageManager

class Application:

    def __init__(self):
        self.make_data_structure()

        self.club = Club("Radnor")
        self.club.load_club("data/local/" + self.club.name)
        self.ui = PageManager(self)
        
        self.is_running = True

    def make_data_structure(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists("data/local"):
            os.mkdir("data/local")   

    def activate(self):
        self.ui.draw()

    def load_match_reports(self):
        return
    
    def quit(self):
        app.club.save_club("data/local/" + app.club.name)
        self.ui.shutdown()

# Refactor this, consider role of page manager vs app, same thing?
app = Application()
app.activate()




    
