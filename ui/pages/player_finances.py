from ui.pages.page_base import PageBase

class FinancesPage(PageBase):
    
    def __init__(self, root, app):
        super().__init__(root, app)
        self.name = "finances"

    def Draw(self):
        print("This is the finances page")
        print("Lee owes bank")