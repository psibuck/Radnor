from tkinter import Entry, Label, StringVar

from src.club.training_venue import TrainingVenue
from ui.wizards.wizard_base import WizardBase

class AddVenueWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root, object)

        Label(self.content_container, text="Venue Name").grid(row=0, column=0)

        Entry(self.content_container, textvariable=self.name_var).grid(row=1,column=0)

        cost_label = Label(self.content_container, text="Cost")
        cost_label.grid(row=0, column=1)

        Entry(self.content_container, textvariable=self.cost_var).grid(row=1, column=1)

    def setup_variables(self):
        self.name_var = StringVar()
        self.cost_var = StringVar()

    def setup_from_object(self, object):
        self.name_var.set(object.name)
        self.cost_var.set(object.cost)

    def construct_object_from_data(self):
        new_venue = TrainingVenue()
        new_venue.name = self.name_var.get()
        if len(new_venue.name) == 0:
            return False, "No venue name set"

        for venue in self.club.training_venues:
            if venue.name == new_venue.name:
                return False, "Venue name already in use"

        new_venue.cost = self.cost_var.get()
        if len(new_venue.cost) == 0:
            return False, "No cost set"
        
        try:
            float(new_venue.cost)
        except ValueError:
            return False, "Cost is not a valid integer"
        return True, new_venue

    def handle_save_pressed(self):
        self.club.training_venues.remove(self.root_object)
        success, new_venue = self.construct_object_from_data()
        if not success:
            self.club.training_venues.append(self.root_object)
            return False, new_venue

        self.club.training_venues.append(new_venue)
        return True, ""
        
    def handle_add_pressed(self):
        success, new_venue = self.construct_object_from_data()
        if not success:
            return False, new_venue

        self.club.training_venues.append(new_venue)
        return True, ""