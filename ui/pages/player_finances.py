from ui.pages.page_base import PageBase

class FinancesPage(PageBase):
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.name = "finances"

    def draw(self):
        print("This is the finances page")
        print("Lee owes bank")