from ui.pages.page_base import PageBase

class FinancesPage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "finances"

    def Draw(self):
        print("This is the finances page")
        print("Lee owes bank")