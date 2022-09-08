from cgitb import text
from statistics import variance
from tkinter import Entry, StringVar

from ui.wizards.wizard_base import WizardBase

class AddClubWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root, object)

        entry = Entry(self, textvariable=self.club_name)
        entry.pack()
        entry.focus()

        short_name_entry = Entry(self, textvariable=self.short_name)
        short_name_entry.pack()

    def setup_variables(self):
        self.club_name = StringVar()
        self.short_name = StringVar()

    def handle_add_pressed(self):
        for club in self.page_manager.app.clubs:
            if club == self.club_name.get():
                return False, "Club with name " + club + " already exists"
        
        self.page_manager.app.add_club(self.club_name.get(), self.short_name.get())
        return True, ""