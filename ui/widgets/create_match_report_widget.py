from tkinter import *
from src.match.match_report import MatchReport, MatchType, Venue
from ui.widgets.object_list import ObjectListWidget

from ui.widgets.player_entry import PlayerEntry

class ButtonInfo:

    def __init__(self, action, icon):
        self.icon = icon
        self.action = action

# SelectTeamWidget allows the user to select a first XI and subs bench from the signed on players
class CreateMatchReportWidget(Frame):

    def __init__(self, available_players, parent, match_report_created_command=None):
        Frame.__init__(self, parent)
        self.pack()
        self.available_players = available_players[:]
        self.first_XI = []
        self.subs = []

        self.on_create = match_report_created_command

        self.available_players_list = ObjectListWidget(self, "Available Players")
        self.available_players_list.grid(row=0, column=0, sticky=N)

        self.selected_players_list = ObjectListWidget(self, "First XI")
        self.selected_players_list.grid(row=0, column=1, sticky=N)

        self.substitute_players_list = ObjectListWidget(self, "Substitutes")
        self.substitute_players_list.grid(row=0, column=2, sticky=N)

        self.selected_match_type = StringVar()
        self.selected_match_type.set(str(MatchType(1)))
        match_type_selector = OptionMenu(self, self.selected_match_type, *list(MatchType))
        match_type_selector.grid(row=0, column = 3, sticky=N)

        self.selected_venue = StringVar()
        self.selected_venue.set(str(Venue(1)))
        venue_selector = OptionMenu(self, self.selected_venue, *list(Venue))
        venue_selector.grid(row=0, column = 4, sticky=N)

        self.SetupObjectLists()

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
        new_match_report.match_type = MatchType[self.selected_match_type.get()]
        new_match_report.venue = Venue[self.selected_venue.get()]
        return new_match_report
        