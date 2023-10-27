from cmath import inf
from datetime import date
from distutils.sysconfig import customize_compiler
from tkinter import *
from turtle import clear

from src.training.report import TrainingReport
from ui.widget_utilities import clear_all_children
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import Table, TableHeader
from ui.wizards.wizard_base import WizardBase

class AddTrainingReportWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root, object)

        info_selector = Frame(self.content_container)
        info_selector.pack(side=TOP)

        date_frame = Frame(info_selector)
        date_frame.pack(side=LEFT)
        
        TableHeader(date_frame, "Date").pack(side=LEFT)
        self.training_date = DateEntry(date_frame)
        self.training_date.pack(side=LEFT)

        venue_frame = Frame(info_selector)
        venue_frame.pack(side=RIGHT)

        TableHeader(venue_frame, "Venue").pack(side=LEFT)     
        if len(self.club.training_venues) > 0:
            venue_names = []
            for venue in self.club.training_venues:
                venue_names.append(venue.name)
            if self.root_object == None:
                self.selected_venue.set(venue_names[0])

            venue_dropdown = OptionMenu(venue_frame, self.selected_venue, *venue_names)
            venue_dropdown.pack(side=LEFT)
        else:
            self.selected_venue.set("None")
            Label(venue_frame, text="No Venues Added").grid(row=1, column=2)

        if self.root_object != None:
            stored_players = self.root_object.attendees[:]
            self.training_date.set_date(self.root_object.date)

        training_frame = Frame(self.content_container)
        training_frame.pack(side=TOP)

        info_frame = Frame(training_frame)
        info_frame.pack(side=TOP)
        TableHeader(info_frame, "Player Pool").pack(side=LEFT)   

    
        self.players_training_count = IntVar()
        self.players_training_count.set(0)
        Label(info_frame, textvariable=self.players_training_count, font=("Arial", 35)).pack(side=LEFT)

        self.player_grid = Frame(training_frame)
        self.player_grid.pack(side=TOP)

        TableHeader(training_frame, "Selected Players").pack(side=TOP)  

        self.selected_player_grid = Frame(training_frame)
        self.selected_player_grid.pack(side=TOP)

        self.custom_area = Frame(self.content_container)
        self.custom_area.pack(side=BOTTOM)

        self.setup_pool_selector()
        self.setup_selected_player_area()
        self.setup_custom_player_area()

    def setup_pool_selector(self):
        clear_all_children(self.player_grid)

        num_per_column = int(len(self.player_pool) / 3)

        row = 0
        column = 0
        for player in self.player_pool:
            if player not in self.selected_players:

                select_button = Checkbutton(self.player_grid, anchor=W, width=10, text=player, command= lambda name = player : self.select_player(name))
                select_button.grid(row=row, column=column)

                if row == num_per_column:
                    row = 0
                    column += 1
                else:
                    row += 1  

    def setup_custom_player_area(self): 
        clear_all_children(self.custom_area)

        self.custom_player_variable = StringVar()
        Entry(self.custom_area, textvariable=self.custom_player_variable).pack(side=LEFT)
        Button(self.custom_area, text="Add", command=lambda: self.add_custom_player()).pack(side=LEFT)

    def add_custom_player(self):
        if self.custom_player_variable != None:
            self.select_player(self.custom_player_variable.get())
            self.custom_player_variable.set("")
            
    def setup_selected_player_area(self):
        clear_all_children(self.selected_player_grid)

        num_per_column = int(len(self.selected_players) / 3)
        row = 0
        column = 0
        for player in self.selected_players:
            player_frame = Frame(self.selected_player_grid)
            player_frame.grid(row=row, column=column)

            Label(player_frame, text=player).pack(side=LEFT)
            Button(player_frame, text="X", command=lambda name=player: self.remove_player(name)).pack(side=LEFT)

            if row == num_per_column:
                row = 0
                column += 1
            else:
                row += 1 

    def setup_variables(self):
        self.selected_venue = StringVar()
        self.selected_players = []
        self.player_pool = self.club.get_player_names()

    def setup_from_object(self, training_report):
        self.selected_players = training_report.attendees
        self.selected_venue.set(training_report.venue)

    def generate_report(self):
        new_report = TrainingReport()
        new_report.attendees = self.selected_players
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
        self.selected_players.append(player_name)

        self.setup_pool_selector()
        self.setup_selected_player_area()

        self.players_training_count.set(self.players_training_count.get() + 1)

    def remove_player(self, player_name):
        if player_name in self.selected_players:
            self.selected_players.remove(player_name)

            self.setup_pool_selector()
            self.setup_selected_player_area()

            self.players_training_count.set(self.players_training_count.get() - 1)

    def handle_save_pressed(self):
        success, new_report = self.generate_report()
        if not success:
            return False, new_report
        self.club.training_reports.remove(self.root_object)
        self.club.add_training_report(new_report)

        return True, ""