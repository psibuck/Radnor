from tkinter import *
from src.match.fixture import MatchType, Venue
from src.match.match_report import MatchReport
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.date_entry import DateEntry
from ui.widgets.player_entry import PlayerEntry
from ui.widgets.table import TableHeader
from ui.wizards.wizard_base import WizardBase

class ButtonInfo:

    def __init__(self, action, icon):
        self.icon = icon
        self.action = action

class NumericEntry(Entry):

    def __init__(self, parent):
        Entry.__init__(self, parent, width=2)

# CreateMatchReportWizard allows users to create a match report
class CreateMatchReportWizard(WizardBase):
    scoreline_row = 0
    opponent_row = 1
    match_type_row = 2
    venue_row = 3
    date_row = 4

    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.pack()
        self.available_players = self.club.players[:]
        self.first_XI = []
        self.subs = []

        self.option_area = Frame(self)
        self.option_area.pack(side=TOP)

        player_area = Frame(self)
        player_area.pack(side=BOTTOM)

        TableHeader(self.option_area, text=self.club.name).grid(row=self.scoreline_row, column=0)
        self.our_scoreline = NumericEntry(self.option_area)
        self.our_scoreline.grid(row=self.scoreline_row, column = 1)
        TableHeader(self.option_area, text="Opposition").grid(row=self.scoreline_row, column=2)
        self.oppo_scoreline = NumericEntry(self.option_area)
        self.oppo_scoreline.grid(row=self.scoreline_row, column = 3)

        TableHeader(self.option_area, "Opposition").grid(row=self.opponent_row, column=0)
        self.selected_opponent = StringVar()
        self.opposition_list = None
        if len(self.club.opponents) > 0:
            self.selected_opponent.set(self.club.opponents[0])
            self.add_opposition_list()

        self.oppo_entry = Entry(self.option_area, text="New Opponent")
        self.oppo_entry.grid(row=self.opponent_row, column=2)
        Button(self.option_area, text="+", command=self.add_opponent).grid(row=self.opponent_row, column=3)

        TableHeader(self.option_area, "Match Type").grid(row=self.match_type_row, column=0)
        self.selected_match_type = StringVar()
        self.selected_match_type.set(str(MatchType(1)))
        match_type_selector = OptionMenu(self.option_area, self.selected_match_type, *list(MatchType))
        match_type_selector.grid(row=self.match_type_row, column=1)

        TableHeader(self.option_area, "Venue").grid(row=self.venue_row, column=0)
        self.selected_venue = StringVar()
        self.selected_venue.set(str(Venue(1)))
        venue_selector = OptionMenu(self.option_area, self.selected_venue, *list(Venue))
        venue_selector.grid(row=self.venue_row, column=1)

        self.date_entry = DateEntry(self.option_area)
        self.date_entry.grid(row=self.date_row, column=0, columnspan=5)

        self.available_players_list = ObjectListWidget(player_area, "Available Players")
        self.available_players_list.grid(row=1, column=0, sticky=N)

        self.selected_players_list = ObjectListWidget(player_area, "First XI")
        self.selected_players_list.grid(row=1, column=1, sticky=N)

        self.substitute_players_list = ObjectListWidget(player_area, "Substitutes")
        self.substitute_players_list.grid(row=1, column=2, sticky=N)

        self.setup_objects_list()

    def add_opposition_list(self):
        if self.opposition_list is not None:
            self.opposition_list.grid_forget()
        self.opposition_list = OptionMenu(self.option_area, self.selected_opponent, *list(self.club.opponents))
        self.opposition_list.grid(row=self.opponent_row, column=1)

    def add_opponent(self):
        opponent_name = self.oppo_entry.get()
        if len(opponent_name) > 0:
            self.club.add_opponent(opponent_name)
            self.selected_opponent.set(opponent_name)

            self.add_opposition_list()
            while self.oppo_entry.get():
                self.oppo_entry.delete(0)

    def select_starter(self, object):
        if len(self.first_XI) < 11:
            self.swap_object(self.available_players, self.first_XI, object)

    def select_sub(self, object):
        if len(self.subs) < 5:
            self.swap_object(self.available_players, self.subs, object)
    
    def deselect_sub(self, object):
        self.swap_object(self.first_XI, self.available_players, object)
        self.swap_object(self.subs, self.available_players, object)
    
    def swap_object(self, current_list, new_list, object):
        if object in current_list:
            current_list.remove(object)
            new_list.append(object)
            new_list.sort()

            self.setup_objects_list()

    def setup_objects_list(self):
        self.setup_list(self.available_players_list, self.available_players, [ButtonInfo(self.select_sub, "SUB"), ButtonInfo(self.select_starter, "XI")]) 
        self.setup_list(self.selected_players_list, self.first_XI, [ButtonInfo(self.deselect_sub, "-")])
        self.setup_list(self.substitute_players_list, self.subs, [ButtonInfo(self.deselect_sub, "-")])
    
    def setup_list(self, list, objects, button_info_list):
        list.clear_widgets()

        widgets = []
        for object in objects:
            entry_widget = PlayerEntry(list, object)

            for button_info in button_info_list:
                new_button = Button(entry_widget, text = button_info.icon, command = lambda w = object, button_action = button_info.action: button_action(w))
                entry_widget.add_control(new_button)
            widgets.append(entry_widget)
        list.setup(widgets)

    def handle_add_pressed(self):
        new_match_report = MatchReport()
        for player in self.first_XI:
            new_match_report.add_starter(player)
        for sub in self.subs:
            new_match_report.add_sub(sub)
        new_match_report.club_goals = self.our_scoreline.get()
        new_match_report.opponent_goals = self.oppo_scoreline.get()
        new_match_report.match_type = MatchType[self.selected_match_type.get()]
        new_match_report.venue = Venue[self.selected_venue.get()]
        new_match_report.opponent = self.selected_opponent.get()
        new_match_report.date = self.date_entry.get_date()
        self.club.add_match_report(new_match_report)
        self.close()        