from tkinter import *
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from ui.pages.page_base import PageBase
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import Table, TableColumn
from ui.widgets.labels import Title
from ui.wizards.add_training_report_wizard import AddTrainingReportWizard
from ui.wizards.add_venue_wizard import AddVenueWizard


class TrainingReports(PageBase):
    name = "Training"

    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.venue_frame = None
        self.training_list_frame = None
        self.trained_players = []

    def setup_content(self):
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight = 10)

        self.venue_frame = Frame(self)
        self.venue_frame.grid(row = 0, column = 0, sticky = "nesw")
        
        self.training_list_frame = Frame(self)
        self.training_list_frame.grid(row = 1, column = 0, sticky = "nesw")

        self.setup_venue_space()
        self.setup_training_space()

    def setup_venue_space(self):
        for widget in self.venue_frame.winfo_children():
            widget.destroy()

        venue_label = Title(self.venue_frame, "Venues")
        venue_label.pack(side = TOP)

        venue_table = Table(self.venue_frame, self.remove_venue, select_func=self.edit_venue)
        venue_table.pack(side = TOP)
        columns = [TableColumn("Name", "name"), TableColumn("Cost", "cost")]
        venue_table.add_columns(columns)

        for venue in self.club.training_venues:
            venue_table.add_object(venue)

        add_venue_button = Button(self.venue_frame, text="+", command=self.add_venue_button_pressed)
        add_venue_button.pack(side = TOP)

    def edit_venue(self, venue):
        self.page_manager.open_wizard(AddVenueWizard, venue)
        
    def remove_venue(self, venue):
        self.club.training_venues.remove(venue)
        self.setup_venue_space()

    def add_venue_button_pressed(self):
        self.page_manager.open_wizard(AddVenueWizard)

    def add_training_button_pressed(self):
        self.page_manager.open_wizard(AddTrainingReportWizard)

    def setup_training_space(self):
        for widget in self.training_list_frame.winfo_children():
            widget.destroy()

        training_list_label = Title(self.training_list_frame, text="Sessions")
        training_list_label.pack(side = TOP)

        training_table = Table(self.training_list_frame, remove_func = self.remove_training_report)
        columns = [TableColumn("Date", function="get_date" ), TableColumn("Num Players", function="GetNumAttendees"), TableColumn("Venue", "venue")]
        training_table.add_columns(columns)
        for report in self.club.training_reports:
            training_table.add_object(report)
        training_table.pack(side=TOP)

        add_training_button = Button(self.training_list_frame, text="+", command=self.add_training_button_pressed)
        add_training_button.pack(side=TOP)

    def remove_training_report(self, report):
        self.club.training_reports.remove(report)
        self.setup_training_space()