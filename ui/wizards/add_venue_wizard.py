from tkinter import Entry, Label

from src.club.training_venue import TrainingVenue
from ui.wizards.wizard_base import WizardBase

class AddVenueWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root)

        Label(self.content_container, text="Venue Name").grid(row=0, column=0)

        self.name_input = Entry(self.content_container)
        self.name_input.grid(row=1,column=0)

        cost_label = Label(self.content_container, text="Cost")
        cost_label.grid(row=0, column=1)

        self.cost_input = Entry(self.content_container)
        self.cost_input.grid(row=1, column=1)

    def handle_add_pressed(self):
        name = self.name_input.get()
        if len(name) == 0:
            return False, "No venue name set"

        for venue in self.club.training_venues:
            if venue.name == name:
                return False, "Venue name already in use"

        cost = self.cost_input.get()
        if len(cost) == 0:
            return False, "No cost set"
        
        try:
            float(cost)
        except ValueError:
            return False, "Cost is not a valid integer"

        self.club.training_venues.append(TrainingVenue(name, cost))
        self.close()

        return True, ""