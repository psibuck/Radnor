from datetime import date
from tkinter import Checkbutton, OptionMenu, Label, StringVar, W

from src.club.training_report import TrainingReport
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import Table, TableColumn
from ui.wizards.wizard_base import WizardBase

class AddTrainingReportWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root, object)

        training_table = Table(self.content_container)
        columns = [TableColumn("Date"), TableColumn("Players"), TableColumn("Venue")]
        training_table.add_columns(columns)
        training_table.grid(row=0, column=0)

        self.training_date = DateEntry(training_table, True)
        self.training_date.grid(row=1, column=0)

        row = 1
        for player in self.club.players:
            select_button = Checkbutton(training_table, text=player.get_name(), command= lambda name = player.get_name() : self.select_player(name))
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
    
    def setup_variables(self):
        self.trained_players = []
        self.selected_venue = StringVar()

        self.training_checkboxes = []

    def setup_from_object(self, training_report):
        self.trained_players = training_report.attendees
        self.selected_venue.set(training_report.venue)

    def generate_report(self):
        new_report = TrainingReport()
        new_report.attendees = self.trained_players
        if new_report.attendees == 0:
            return False, "No trainees added to training report"
        
        new_report.date = self.training_date.get_date()
        if new_report.date > date.today():
            return False, "Date cannot be in the future"

        for venue in self.club.training_venues:
            if venue.name == self.selected_venue.get():
                new_report.venue = venue
                break

        if new_report.venue == None:
            return False, "No venue set, if you need to add some cancel and come back"
        return True, new_report
    
    def handle_add_pressed(self):
        success, new_report = self.generate_report()
        if not success:
            return False, new_report

        self.club.add_training_report(new_report)
        return True, ""

    def select_player(self, player_name):
        if player_name in self.trained_players:
            self.trained_players.remove(player_name)
        else:
            self.trained_players.append(player_name)

    def handle_save_pressed(self):
        success, new_report = self.generate_report()
        if not success:
            return False, new_report
        self.club.training_reports.remove(self.root_object)
        self.club.add_training_report(new_report)

        return True, ""