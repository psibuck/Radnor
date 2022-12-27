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

        transactions_display = Frame(self, width=350)
        transactions_display.pack(side=TOP)

        in_transactions = Frame(transactions_display)
        in_transactions.pack(side = LEFT, anchor=N)
        Label(in_transactions, text="IN", font=("Arial", 30)).pack(side=TOP)

        out_transactions = Frame(transactions_display)
        out_transactions.pack(side = RIGHT, anchor=N)
        Label(out_transactions, text="OUT", font=("Arial", 30)).pack(side=TOP)

        total = 0
        for transaction in self.club.get_player_transaction_list(self.player):
            if transaction.get_amount() > 0:
                Label(in_transactions, text = transaction).pack(side=TOP)
            else:
                Label(out_transactions, text = transaction).pack(side=TOP)

            total += transaction.get_amount()
        
        Label(self, text="TOTAL: " + get_amount_string(total), font=("Arial", 30)).pack(side=BOTTOM)



