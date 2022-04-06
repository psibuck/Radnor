from ui.pages.home import *
from ui.pages.player_finances import FinancesPage
from ui.pages.player_stats import StatsPage

class PageManager:

    def __init__(self):
        self.page_index = 0
        self.home_page = "home"
        self.pages = []
        self.pages.append(HomePage(self))
        self.pages.append(StatsPage(self))
        self.pages.append(FinancesPage(self))

    def SwitchPage(self, page_index):
        if page_index < len(self.pages):
            self.page_index = page_index

    def PrintControls(self):
        index = 0
        message = ""
        for page in self.pages:
            message += "Press " + str(index + 1) + " for " + self.pages[index].name + "\n"
            index += 1
        print(message)
    
    def HandleInput(self, input):
        page_to_switch_to = int(input)
        self.SwitchPage(page_to_switch_to - 1)  

    def Draw(self):
        self.PrintControls()
        self.pages[self.page_index].Draw()
        self.GetInput()
        
    def GetInput(self):
        player_input = input("So what do you want to do?")
        self.pages[self.page_index].HandleInput(player_input)