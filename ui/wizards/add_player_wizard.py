from datetime import date
from tkinter import BooleanVar, Checkbutton, Entry, StringVar, TOP

from src.club.player import Player
from ui.widgets.date_entry import DateEntry
from ui.wizards.wizard_base import WizardBase

class AddPlayerWizard(WizardBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.first_name = StringVar()
        self.surname = StringVar()
        self.signed_on = BooleanVar()
        self.signed_on.set(False)

        Entry(root, textvariable=self.first_name).pack(side = TOP)
        Entry(root, textvariable=self.surname).pack(side = TOP)
        Checkbutton(root, text="Signed On", variable=self.signed_on).pack(side=TOP)

        self.date_entry = DateEntry(root, end_year = date.today().year - 16, years_to_show=50)
        self.date_entry.pack(side = TOP)

    def handle_add_pressed(self):
        new_player = Player()
        new_player.first_name = self.first_name.get()
        new_player.surname = self.surname.get()
        new_player.dob = self.date_entry.get_date()
        new_player.is_signed_on = self.signed_on.get()
        if len(new_player.first_name) == 0:
            return False, "No first name entered"
        elif len(new_player.surname) == 0:
            return False, "No surname entered"

        return self.club.add_player(new_player)

