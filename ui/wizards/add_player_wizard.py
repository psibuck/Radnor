from datetime import date
from tkinter import BooleanVar, Checkbutton, Entry, StringVar, TOP

from src.club.player import Player
from ui.widgets.date_entry import DateEntry
from ui.wizards.wizard_base import WizardBase

class AddPlayerWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        self.first_name = StringVar()
        self.surname = StringVar()
        self.signed_on = BooleanVar()
        self.signed_on.set(False)

        entry = Entry(root, textvariable=self.first_name)
        entry.pack(side = TOP)
        entry.focus()
        
        Entry(root, textvariable=self.surname).pack(side = TOP)
        Checkbutton(root, text="Signed On", variable=self.signed_on).pack(side=TOP)

        self.date_entry = DateEntry(root, end_year = date.today().year - 16, years_to_show=50)
        self.date_entry.pack(side = TOP)

        super().__init__(manager, root, object)

    def setup_from_object(self, object):
        self.first_name.set(object.first_name)
        self.surname.set(object.surname)
        self.signed_on.set(object.is_signed_on)
        self.date_entry.set_date(object.dob)

    def construct_player_from_data(self):
        new_player = Player()
        new_player.first_name = self.first_name.get()
        new_player.surname = self.surname.get()
        new_player.dob = self.date_entry.get_date()
        new_player.is_signed_on = self.signed_on.get()

        if len(new_player.first_name) == 0:
            return False, "No first name entered"
        elif len(new_player.surname) == 0:
            return False, "No surname entered"
        return True, new_player

    def handle_add_pressed(self):            
        success, new_player = self.construct_player_from_data()
        if not success:
            return success, new_player

        return self.club.add_player(new_player)

    def handle_edit_pressed(self):
        success, new_player = self.construct_player_from_data()
        if not success:
            return success, new_player

        if self.root_object == None:
            return False, "ERROR: attempting to update player but no root object set"

        return self.club.update_player(self.root_object, new_player)

    def handle_delete_pressed(self):
        if self.root_object == None:
            return False, "ERROR: on_delete_pressed but there is no root object"
        return self.club.remove_player(self.root_object)
