from cgitb import text
from statistics import variance
from tkinter import Entry, StringVar

from ui.wizards.wizard_base import WizardBase

class AddClubWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root, object)

        self.club_name = StringVar()
        Entry(self, textvariable=self.club_name).pack()

    def setup_variables(self):
        self.club_name = StringVar()

    def handle_add_pressed(self):
        for club in self.page_manager.app.clubs:
            if club == self.club_name.get():
                return False, "Club with name " + club + " already exists"
        
        self.page_manager.app.add_club(self.club_name.get())
        return True, ""