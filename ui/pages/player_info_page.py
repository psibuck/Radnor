from tkinter import *
from ui.pages.page_base import PageBase

class PlayerView(PageBase):

    def __init__(self, manager, root, player):
        super().__init__(manager, root)

        self.player = player
        self.setup_content()


    def setup_content(self):

        Label(self, text=self.player.get_name(), font=("Arial", 30)).pack(side=TOP)


