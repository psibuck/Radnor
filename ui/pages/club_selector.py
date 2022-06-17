from tkinter import Label
from ui.pages.page_base import PageBase

class ClubSelector(PageBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root)

    def setup_content(self):
        for club in self.page_manager.app.clubs:
            Label(self, text=club).pack()