from tkinter import *
from src.match.match_report import MatchReport, MatchType, Venue
from ui.widgets.object_list import ObjectListWidget

from ui.widgets.player_entry import PlayerEntry
from ui.widgets.table import TableHeader

class ButtonInfo:

    def __init__(self, action, icon):
        self.icon = icon
        self.action = action

class NumericEntry(Entry):

    def __init__(self, parent):
        Entry.__init__(self, parent)

# SelectTeamWidget allows the user to select a first XI and subs bench from the signed on players
class CreateMatchReportWidget(Frame):
    scoreline_row = 0
    opponent_row = 1
    match_type_row = 2
    venue_row = 3

    def __init__(self, club, parent, match_report_created_command=None):
        Frame.__init__(self, parent)
        self.club = club
        self.pack()
        self.available_players = club.players[:]
        self.first_XI = []
        self.subs = []

        self.on_create = match_report_created_command

        self.option_area = Frame(self)
        self.option_area.pack(side=TOP)

        player_area = Frame(self)
        player_area.pack(side=BOTTOM)


        Label(self.option_area, text=self.club.name).grid(row=self.scoreline_row, column=0)
        self.our_scoreline = NumericEntry(self.option_area)
        self.our_scoreline.grid(row=self.scoreline_row, column = 1)
        Label(self.option_area, text="Opposition").grid(row=self.scoreline_row, column=2)
        self.oppo_scoreline = NumericEntry(self.option_area)
        self.oppo_scoreline.grid(row=self.scoreline_row, column = 3)

        TableHeader(self.option_area, "Opposition").grid(row=self.opponent_row, column=0)
        self.selected_opponent = StringVar()
        self.opposition_list = None
        if len(club.opponents) > 0:
            self.selected_opponent.set(club.opponents[0])
            self.AddOppositionList()

        self.oppo_entry = Entry(self.option_area, text="New Opponent")
        self.oppo_entry.grid(row=self.opponent_row, column=2)
        Button(self.option_area, text="+", command=self.AddOpponent).grid(row=self.opponent_row, column=3)

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

        self.available_players_list = ObjectListWidget(player_area, "Available Players")
        self.available_players_list.grid(row=1, column=0, sticky=N)

        self.selected_players_list = ObjectListWidget(player_area, "First XI")
        self.selected_players_list.grid(row=1, column=1, sticky=N)

        self.substitute_players_list = ObjectListWidget(player_area, "Substitutes")
        self.substitute_players_list.grid(row=1, column=2, sticky=N)

        self.SetupObjectLists()

    def AddOppositionList(self):
        if self.opposition_list is not None:
            self.opposition_list.grid_forget()
        self.opposition_list = OptionMenu(self.option_area, self.selected_opponent, *list(self.club.opponents))
        self.opposition_list.grid(row=self.opponent_row, column=1)

    def AddOpponent(self):
        opponent_name = self.oppo_entry.get()
        if len(opponent_name) > 0:
            self.club.AddOpponent(opponent_name)
            self.selected_opponent.set(opponent_name)

            self.AddOppositionList()
            while self.oppo_entry.get():
                self.oppo_entry.delete(0)

    def SelectStarter(self, object):
        if len(self.first_XI) < 11:
            self.SwapObject(self.available_players, self.first_XI, object)

    def SelectSub(self, object):
        if len(self.subs) < 5:
            self.SwapObject(self.available_players, self.subs, object)
    
    def DeselectPlayer(self, object):
        self.SwapObject(self.first_XI, self.available_players, object)
        self.SwapObject(self.subs, self.available_players, object)
    
    def SwapObject(self, current_list, new_list, object):
        if object in current_list:
            current_list.remove(object)
            new_list.append(object)
            new_list.sort()

            self.SetupObjectLists()

    def SetupObjectLists(self):
        self.SetupList(self.available_players_list, self.available_players, [ButtonInfo(self.SelectSub, "SUB"), ButtonInfo(self.SelectStarter, "XI")]) 
        self.SetupList(self.selected_players_list, self.first_XI, [ButtonInfo(self.DeselectPlayer, "-")])
        self.SetupList(self.substitute_players_list, self.subs, [ButtonInfo(self.DeselectPlayer, "-")])
    
    def SetupList(self, list, objects, button_info_list):
        list.ClearWidgets()

        widgets = []
        for object in objects:
            entry_widget = PlayerEntry(list, object)

            for button_info in button_info_list:
                new_button = Button(entry_widget, text = button_info.icon, command = lambda w = object, button_action = button_info.action: button_action(w))
                entry_widget.AddControl(new_button)
            widgets.append(entry_widget)
        list.Setup(widgets)

    def CreateMatchReport(self):
        new_match_report = MatchReport()
        for player in self.first_XI:
            new_match_report.AddStarter(player)
        for sub in self.subs:
            new_match_report.AddSub(sub)
        new_match_report.club_goals = self.our_scoreline.get()
        new_match_report.opponent_goals = self.oppo_scoreline.get()
        new_match_report.match_type = MatchType[self.selected_match_type.get()]
        new_match_report.venue = Venue[self.selected_venue.get()]
        new_match_report.opponent = self.selected_opponent.get()
        return new_match_report
        