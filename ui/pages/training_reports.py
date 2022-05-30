from tkinter import *
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from ui.pages.page_base import PageBase
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import Table, TableColumn
from ui.widgets.labels import Title

import random

class TrainingReports(PageBase):
    name = "Training"

    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.venue_frame = None
        self.training_list_frame = None
        self.creator_space = None
        self.trained_players = []
        self.selected_venue = StringVar()

    def setup_content(self):
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight = 10)

        self.venue_frame = Frame(self)
        self.venue_frame.grid(row = 0, column = 0, sticky = "nesw")
        
        self.training_list_frame = Frame(self)
        self.training_list_frame.grid(row = 1, column = 0, sticky = "nesw")
        
        self.creator_space = Frame(self)
        self.creator_space.grid(row=0, column=1, sticky = "nesw")

        self.setup_venue_space()
        self.setup_training_space()

    def setup_venue_space(self):
        for widget in self.venue_frame.winfo_children():
            widget.destroy()

        venue_label = Title(self.venue_frame, "Venues")
        venue_label.pack(side = TOP)

        venue_table = Table(self.venue_frame, self.remove_venue)
        venue_table.pack(side = TOP)
        columns = [TableColumn("Name", "name"), TableColumn("Cost", "cost")]
        venue_table.add_columns(columns)

        for venue in self.club.training_venues:
            venue_table.add_object(venue)

        add_venue_button = Button(self.venue_frame, text="+", command=self.add_venue_button_pressed)
        add_venue_button.pack(side = TOP)

    def remove_venue(self, venue):
        self.clear_creator_space()
        self.club.training_venues.remove(venue)
        self.setup_venue_space()

    def add_venue_button_pressed(self):
        self.clear_creator_space()
        
        name_label = Label(self.creator_space, text="Venue Name")
        name_label.grid(row=0, column=0)
        name_input = Entry(self.creator_space)
        name_input.grid(row=1,column=0)

        cost_label = Label(self.creator_space, text="Cost")
        cost_label.grid(row=0, column=1)

        cost_input = Entry(self.creator_space)
        cost_input.grid(row=1, column=1)

        save_button = Button(self.creator_space, text="SAVE", command = lambda: self.add_venue(name_input.get(), cost_input.get()))
        save_button.grid(row=2, column=2)

    def add_training_button_pressed(self):
        self.clear_creator_space()

        training_table = Table(self.creator_space)
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

        save_button = Button(self.creator_space, text="Save", command=self.add_training_session)
        save_button.grid(row=1, column=3)

    def select_player(self, player_name):
        if player_name in self.trained_players:
            self.trained_players.remove(player_name)
        else:
            self.trained_players.append(player_name)

    def add_training_session(self):
        new_report = TrainingReport()
        new_report.attendees = self.trained_players

        for venue in self.club.training_venues:
            if venue.name == self.selected_venue.get():
                new_report.venue = venue
                break
        self.club.add_training_report(new_report)
        self.trained_players = []
        self.setup_training_space()
        self.clear_creator_space()

    def add_venue(self, venue_name, venue_cost):
        self.clear_creator_space()
        
        new_venue = TrainingVenue(venue_name, venue_cost)
        self.club.training_venues.append(new_venue)

        self.setup_venue_space()

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

    def clear_creator_space(self):
        for widget in self.creator_space.winfo_children():
            widget.destroy()

    def remove_training_report(self, report):
        self.clear_creator_space()
        self.club.training_reports.remove(report)
        self.setup_training_space()