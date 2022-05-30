from tkinter import Entry, Label

from src.club.training_venue import TrainingVenue
from ui.wizards.wizard_base import WizardBase

class AddVenueWizard(WizardBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        Label(self, text="Venue Name").grid(row=0, column=0)

        self.name_input = Entry(self)
        self.name_input.grid(row=1,column=0)

        cost_label = Label(self, text="Cost")
        cost_label.grid(row=0, column=1)

        self.cost_input = Entry(self)
        self.cost_input.grid(row=1, column=1)

    def handle_add_pressed(self):
        self.club.training_venues.append(TrainingVenue(self.name_input.get(), self.cost_input.get()))
        self.close()