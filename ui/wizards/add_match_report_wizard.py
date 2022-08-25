from datetime import date
from tkinter import *
from src.match.fixture import MatchType, Venue
from src.match.goal import Goal
from src.match.match_report import MatchReport
from ui import widget_utilities
from ui.widgets.goal_display import GoalDisplay
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.date_entry import DateEntry
from ui.widgets.player_entry import PlayerEntry
from ui.widgets.scrollframe import ScrollFrame
from ui.widgets.table import TableHeader
from ui.wizards.wizard_base import WizardBase
from src.utilities.constants import MAX_SUBS, NUM_STARTERS

class ButtonInfo:

    def __init__(self, action, icon):
        self.icon = icon
        self.action = action

class NumericEntry(Entry):

    def __init__(self, parent, variable = None):
        Entry.__init__(self, parent, width=2, textvariable = variable)

# AddMatchReportWizard allows users to create a match report
class AddMatchReportWizard(WizardBase):
    scoreline_row = 0
    opponent_row = 1
    match_type_row = 2
    venue_row = 3
    date_row = 4

    def __init__(self, manager, root, object=None):

        self.our_goals = IntVar(manager.root)
        self.our_goals.set(0)

        self.opponent_goals = IntVar(manager.root)
        self.opponent_goals.set(0)

        self.available_players = manager.app.club.players[:]
        self.starters = []
        self.subs = []

        self.selected_opponent = StringVar()
        self.selected_venue = StringVar()
        self.selected_venue.set(str(Venue(1)))
        self.selected_match_type = StringVar()
        self.selected_match_type.set(str(MatchType(1)))
        self.selected_date: date = date.today()

        if len(manager.app.club.opponents) > 0:
            self.selected_opponent.set(manager.app.club.opponents[0])

        super().__init__(manager, root, object)

        self.option_area = Frame(self.content_container)
        self.option_area.pack(fill=BOTH, expand=YES)
        
        list_area = LabelFrame(self.content_container)
        list_area.pack(side=BOTTOM, fill=BOTH, expand=YES)

        player_area = Frame(list_area)
        player_area.pack(side=LEFT)

        self.goal_area = GoalDisplay(list_area, manager)
        self.goal_area.pack(side=RIGHT)

        self.our_goals.trace("w", self.goal_area.handle_goals_update)

        TableHeader(self.option_area, text=self.club.name).grid(row=self.scoreline_row, column=0)
        NumericEntry(self.option_area, self.our_goals).grid(row=self.scoreline_row, column = 1)
        TableHeader(self.option_area, text="Opposition").grid(row=self.scoreline_row, column=2)
        self.oppo_scoreline = NumericEntry(self.option_area, self.opponent_goals)
        self.oppo_scoreline.grid(row=self.scoreline_row, column = 3)

        TableHeader(self.option_area, "Opposition").grid(row=self.opponent_row, column=0)
        self.opposition_list = None
        self.add_opposition_list()

        self.oppo_entry = Entry(self.option_area, text="New Opponent")
        self.oppo_entry.grid(row=self.opponent_row, column=2)
        Button(self.option_area, text="+", command=self.add_opponent).grid(row=self.opponent_row, column=3)

        TableHeader(self.option_area, "Match Type").grid(row=self.match_type_row, column=0)
        match_type_selector = OptionMenu(self.option_area, self.selected_match_type, *list(MatchType))
        match_type_selector.grid(row=self.match_type_row, column=1)

        TableHeader(self.option_area, "Venue").grid(row=self.venue_row, column=0)
        venue_selector = OptionMenu(self.option_area, self.selected_venue, *list(Venue))
        venue_selector.grid(row=self.venue_row, column=1)

        self.date_entry = DateEntry(self.option_area, default_date = self.selected_date, years_to_show=2)
        self.date_entry.grid(row=self.date_row, column=0, columnspan=5)

        self.squad_display = ScrollFrame(player_area, width=150)
        self.squad_display.grid(row=1, column=0, sticky=NW)

        self.starter_display = Frame(player_area)
        self.starter_display.grid(row=1, column=1, sticky=N)

        self.sub_display = Frame(player_area)
        self.sub_display.grid(row=1, column=2, sticky=N)

        self.setup_player_lists()

    def add_list(self, container, name, list):
        name_frame = Frame(container)
        name_frame.pack(side=TOP)

        TableHeader(name_frame, text=name).pack(side=LEFT)
        Label(name_frame, text=len(list)).pack(side=LEFT)

        for player in list:
            player_frame = Frame(container)
            player_frame.pack(side=TOP)
            Label(player_frame, text=player).pack(side=LEFT, expand=YES)
            Button(player_frame, text="-", command= lambda player = player : self.remove_player(player)).pack(side=RIGHT)

    def setup_player_lists(self):
        self.squad_display.clear_children()
        widget_utilities.clear_all_children(self.starter_display)
        widget_utilities.clear_all_children(self.sub_display)

        for player in self.available_players:
            player_frame = Frame(self.squad_display.content_area)
            player_frame.pack(side=TOP)

            Label(player_frame, text=player).pack(side=LEFT, expand=YES)
            Button(player_frame, text="SUB", command=lambda player = player : self.add_player_to_subs(player) ).pack(side=RIGHT)
            Button(player_frame, text="XI", command=lambda player = player : self.add_player_to_starters(player)).pack(side=RIGHT)

        self.add_list(self.starter_display, "FIRST XI", self.starters)
        self.add_list(self.sub_display, "SUBS", self.subs)

    def populate_player_list(self, initial_list, additive_list, player_list):
        for player_name in initial_list:
            player = self.club.get_player_by_name(player_name)
            if player != None:
                additive_list.append(player)
                player_list.remove(player)

    def add_player_to_subs(self, player):
        self.subs.append(player)
        self.available_players.remove(player)
        self.setup_player_lists()

    def add_player_to_starters(self, player):
        if len(self.starters) < 11:
            self.starters.append(player)
            self.available_players.remove(player)
            self.setup_player_lists()

    def remove_player(self, player):
        if player in self.starters:
            self.starters.remove(player)
        else:
            self.subs.remove(player)
        self.available_players.append(player)
        self.setup_player_lists()

    def setup_from_object(self, object: MatchReport):
        players = self.club.players[:]

        self.selected_opponent.set(object.opponent)
        self.selected_venue.set(str(object.venue))
        self.selected_match_type.set(str(object.match_type))
        self.selected_date = object.date

        self.populate_player_list(object.starting_lineup, self.starters, players)
        self.populate_player_list(object.subs, self.subs, players)
        self.available_players = players
        
        self.our_goals.set(object.club_goals)
        self.opponent_goals.set(object.opponent_goals)
        
    def add_opposition_list(self):
        if len(self.club.opponents) > 0:
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
        if len(self.starters) < 11:
            self.swap_object(self.available_players, self.starters, object)

    def select_sub(self, object):
        if len(self.subs) < MAX_SUBS or MatchType[self.selected_match_type.get()] == MatchType.FRIENDLY:
            self.swap_object(self.available_players, self.subs, object)
    
    def deselect_sub(self, object):
        self.swap_object(self.starters, self.available_players, object)
        self.swap_object(self.subs, self.available_players, object)
    
    def swap_object(self, current_list, new_list, object):
        if object in current_list:
            current_list.remove(object)
            new_list.append(object)
            new_list.sort()

            self.setup_objects_list()

    def setup_objects_list(self):
        self.setup_list(self.available_players_list, self.available_players, [ButtonInfo(self.select_sub, "SUB"), ButtonInfo(self.select_starter, "XI")]) 
        self.setup_list(self.selected_players_list, self.starters, [ButtonInfo(self.deselect_sub, "-")])
        self.setup_list(self.substitute_players_list, self.subs, [ButtonInfo(self.deselect_sub, "-")])
        self.goal_area.update_player_list(self.get_selected_players())
    
    def get_selected_players(self):
        return self.starters[:] + self.subs[:]

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

    def setup_variables(self):
        return super().setup_variables()

    def handle_save_pressed(self):
        success, report = self.construct_report()
        if not success:
            return False, report

        self.club.remove_match_report(self.root_object)
        self.club.add_match_report(report)
        return True, ""

    def handle_delete_pressed(self):
        return super().handle_delete_pressed()

    def handle_add_pressed(self):
        success, report = self.construct_report()
        if not success:
            return False, report

        self.club.add_match_report(report)
        return True, report

    def construct_report(self):
        new_report = MatchReport()
        new_report.match_type = MatchType[self.selected_match_type.get()]
        if len(self.starters) != NUM_STARTERS:
            return False, "Not enough starters added to match report"
        if len(self.subs) > MAX_SUBS and new_report.match_type != MatchType.FRIENDLY:
            return False, "Too many players on subs bench"

        for player in self.starters:
            new_report.add_starter(player)
        for sub in self.subs:
            new_report.add_sub(sub)
            
        new_report.club_goals = self.our_goals.get()
        new_report.opponent_goals = self.opponent_goals.get()
        new_report.venue = Venue[self.selected_venue.get()]
        new_report.opponent = self.selected_opponent.get()
        new_report.date = self.date_entry.get_date()

        for goal in self.goal_area.goal_entries:
            new_goal = Goal(goal.goalscorer, goal.assister, "test goal description")
            new_report.add_goal(new_goal)

        return True, new_report