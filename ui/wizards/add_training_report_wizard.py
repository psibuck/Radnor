from tkinter import Button, Checkbutton, OptionMenu, Label, StringVar, W

from src.club.training_report import TrainingReport
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import Table, TableColumn
from ui.wizards.wizard_base import WizardBase

class AddTrainingReportWizard(WizardBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.trained_players = []
        self.selected_venue = StringVar()

        training_table = Table(self)
        columns = [TableColumn("Date"), TableColumn("Players"), TableColumn("Venue")]
        training_table.add_columns(columns)
        training_table.grid(row=0, column=0)

        self.training_date = DateEntry(training_table, True)
        self.training_date.grid(row=1, column=0)

        self.training_checkboxes = []
        row = 1
        for player in self.club.players:
            select_button = Checkbutton(training_table, text=player.name, command= lambda name = player.name : self.select_player(name))
            select_button.grid(row=row, column=1, sticky=W)
            self.training_checkboxes.append(select_button)        
            row += 1
        
        if len(self.club.training_venues) > 0:
            venue_names = []
            for venue in self.club.training_venues:
                venue_names.append(venue.name)
            self.selected_venue.set(venue_names[0])
            venue_dropdown = OptionMenu(training_table, self.selected_venue, *venue_names)
            venue_dropdown.grid(row=1, column=2)
        else:
            self.selected_venue.set("None")
            Label(training_table, text="No Venues Added").grid(row=1, column=2)

    def handle_add_pressed(self):
        new_report = TrainingReport()
        new_report.attendees = self.trained_players
        new_report.date = self.training_date.get_date()
        for venue in self.club.training_venues:
            if venue.name == self.selected_venue.get():
                new_report.venue = venue
                break
        self.club.add_training_report(new_report)
        self.close()

    def select_player(self, player_name):
        if player_name in self.trained_players:
            self.trained_players.remove(player_name)
        else:
            self.trained_players.append(player_name)