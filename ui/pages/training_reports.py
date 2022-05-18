from tkinter import *
from src.club.training_report import TrainingReport
from src.club.training_venue import TrainingVenue
from ui.pages.page_base import PageBase

import random

class TrainingReports(PageBase):
    name = "Training"

    def __init__(self, root, app):
        super().__init__(root, app)
        self.venue_frame = None
        self.training_list_frame = None
        self.creator_space = None
        self.trained_players = []

    def SetupContent(self):
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)

        self.venue_frame = Frame(self, bg = "red")
        self.venue_frame.grid(row = 0, column = 0, sticky = "nesw")
        
        self.training_list_frame = Frame(self, bg = "green")
        self.training_list_frame.grid(row = 0, column = 1, sticky = "nesw")
        
        self.creator_space = Frame(self, bg="black")
        self.creator_space.grid(row=1, columnspan=2, sticky = "nesw")
        
        venue_label = Label(self.creator_space, text="Creator")
        venue_label.pack(side = TOP)

        self.SetupVenueSpace()
        self.SetupTrainingSpace()

    def SetupVenueSpace(self):
        for widget in self.venue_frame.winfo_children():
            widget.destroy()

        venue_label = Label(self.venue_frame, text="Venues")
        venue_label.pack(side = TOP)

        venue_space = Frame(self.venue_frame)
        venue_space.pack(side=TOP)

        row = 0
        for venue in self.club.training_venues:
            venue_name = Label(venue_space, text=venue.name)
            venue_name.grid(row=row, column=0)

            venue_cost_string = "£" + str(venue.cost)
            venue_cost = Label(venue_space, text=venue_cost_string)
            venue_cost.grid(row=row, column=1)
            row += 1

        add_venue_button = Button(venue_space, text="+", command=self.AddVenueButtonPressed)
        add_venue_button.grid(row=row+2, column = 0, columnspan=2)

    def AddVenueButtonPressed(self):
        self.ClearCreatorSpace()
        
        name_label = Label(self.creator_space, text="Venue Name")
        name_label.grid(row=0, column=0)
        name_input = Entry(self.creator_space)
        name_input.grid(row=1,column=0)

        cost_label = Label(self.creator_space, text="Cost")
        cost_label.grid(row=0, column=1)

        cost_input = Entry(self.creator_space)
        cost_input.grid(row=1, column=1)

        save_button = Button(self.creator_space, text="SAVE", command = lambda: self.AddVenue(name_input.get(), cost_input.get()))
        save_button.grid(row=2, column=2)

    def AddTrainingButtonPressed(self):
        self.ClearCreatorSpace()

        self.training_checkboxes = []
        row = 0
        for player in self.club.players:
            select_button = Checkbutton(self.creator_space, text=player.name, command= lambda name = player.name : self.SelectPlayer(name))
            select_button.grid(row=row, column=0)
            self.training_checkboxes.append(select_button)        
            row += 1
        
        save_button = Button(self.creator_space, text="Save", command=self.AddTrainingSession)
        save_button.grid(row=0, column=1)

        #https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter

    def SelectPlayer(self, player_name):
        if player_name in self.trained_players:
            self.trained_players.remove(player_name)
        else:
            self.trained_players.append(player_name)

    def AddTrainingSession(self):
        new_report = TrainingReport()
        new_report.attendees = self.trained_players
        new_report.venue = random.choice(self.club.training_venues)
        self.club.training_reports.append(new_report)
        self.trained_players = []
        self.SetupTrainingSpace()
        self.ClearCreatorSpace()

    def AddVenue(self, venue_name, venue_cost):
        self.ClearCreatorSpace()
        
        new_venue = TrainingVenue(venue_name, venue_cost)
        self.club.training_venues.append(new_venue)

        self.SetupVenueSpace()

    def AddHeader(self, table, name, column):
        new_header = Label(table, text=name)
        new_header.grid(row=0, column=column)

    def SetupTrainingSpace(self):
        for widget in self.training_list_frame.winfo_children():
            widget.destroy()

        training_list_label = Label(self.training_list_frame, text="Training Sessions")
        training_list_label.pack(side = TOP)

        training_list = Frame(self.training_list_frame)
        training_list.pack(side=TOP)

        row = 0
        column = 0
        
        self.AddHeader(training_list, "Num Attendees", column)
        column += 1
        self.AddHeader(training_list, "Venue", column)

        row += 1
        for report in self.club.training_reports:
            num_attendees = Label(training_list, text=str(len(report.attendees)))
            num_attendees.grid(row=row, column = 0)

            label = Label(training_list, text=report.venue.name)
            label.grid(row = row, column = 1)
            row += 1

        add_training_button = Button(training_list, text="+", command=self.AddTrainingButtonPressed)
        add_training_button.grid(row=row, column=0)

    def ClearCreatorSpace(self):
        for widget in self.creator_space.winfo_children():
            widget.destroy()