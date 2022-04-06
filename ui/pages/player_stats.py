from ui.pages.page_base import PageBase

class StatsPage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "stats"

    def Draw(self):
        print("This is the stats page")
        print("Tom goals: 0")

    def HandleInput(self, input):

        super.HandleInput(input)