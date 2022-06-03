from datetime import date
from tkinter import Entry, TOP

from src.club.player import Player
from ui.widgets.date_entry import DateEntry
from ui.wizards.wizard_base import WizardBase

class AddPlayerWizard(WizardBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.input_box = Entry(root)
        self.input_box.pack(side = TOP)

        self.date_entry = DateEntry(root, end_year = date.today().year - 16, years_to_show=50)
        self.date_entry.pack(side = TOP)

    def handle_add_pressed(self):
        new_player = Player()
        new_player.name = self.input_box.get()
        new_player.dob = self.date_entry.get_date()
        if len(new_player.name) == 0:
            return "No Player Name Entered", False

        return self.club.add_player(new_player)

