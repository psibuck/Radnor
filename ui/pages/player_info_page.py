from tkinter import *
from src.finances.financial_utilities import get_amount_string
from ui.pages.page_base import PageBase

class PlayerView(PageBase):

    def __init__(self, manager, root, player):
        super().__init__(manager, root)

        self.player = player
        self.setup_content()


    def setup_content(self):
        Label(self, text=self.player.get_name(), font=("Arial", 30)).pack(side=TOP)

        transactions_list = Frame(self)
        transactions_list.pack(side = TOP)

        total = 0
        for transaction in self.club.get_player_transaction_list(self.player):
            Label(transactions_list, text = transaction).pack(side=TOP)
            total += transaction.get_amount()
        
        Label(self, text="TOTAL: " + get_amount_string(total), font=("Arial", 30)).pack(side=TOP)



