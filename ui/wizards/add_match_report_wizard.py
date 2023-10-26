"""Contains the classes and logic for the UI that allows us to create and edit match reports"""
from datetime import date
from tkinter import BOTH, BOTTOM, Button, Entry, Frame, IntVar, Label, LabelFrame, LEFT, N, NW, OptionMenu, RIGHT, StringVar, TOP, YES
import src.match.fixture as Fixture
from src.club.player import Player
from src.match.fixture import MatchType, Venue
from src.match.goal import Goal
from src.match.match_report import MatchReport
from ui import widget_utilities
from ui.widgets.goal_display import GoalDisplay
from ui.widgets.date_entry import DateEntry
from ui.widgets.player_entry import PlayerEntry
from ui.widgets.scrollframe import ScrollFrame
from ui.widgets.table import TableHeader
from ui.wizards.wizard_base import WizardBase
from src.utilities.constants import MAX_SUBS, NUM_STARTERS

class ButtonInfo:
    """Data wrapper that packages the info we need to display a button"""

    def __init__(self, action, icon):
        self.icon = icon
        self.action = action

class NumericEntry(Entry):
    """An extension of entry that defines the width as 2 and validates the entry is an integer"""

    def __init__(self, parent, variable = None):
        Entry.__init__(self, parent, width=2, validatecommand=self.validate, textvariable = variable)

    def validate(self, *args) -> bool:
        """Returns true if the value added is a numeric value"""
        print("NumericEntry validate called")
        for arg in args:
            print(arg)
        return True


class AddMatchReportWizard(WizardBase):
    """AddMatchReportWizard allows users to create a match report"""
    scoreline_row = 0
    opponent_row = 1
    match_type_row = 2
    venue_row = 3
    date_row = 4

    def __init__(self, manager, root, base_object: MatchReport=None):

        self.report = base_object
        if self.report is None:
            self.report = MatchReport()
        
        self.our_goals = IntVar(manager.root)
        self.opponent_goals = IntVar(manager.root)

        self.available_players = manager.app.club.players[:]

        self.selected_opponent = StringVar()
        self.selected_venue = StringVar()
        self.selected_venue.trace_add("write", self.handle_venue_change)
        self.selected_match_type = StringVar()
        self.selected_match_type.trace_add("write", self.handle_match_type_change)
        self.selected_date: date = date.today()

        if len(manager.app.club.opponents) > 0:
            self.selected_opponent.set(manager.app.club.opponents[0])

        super().__init__(manager, root, base_object)

        self.option_area = Frame(self.content_container)
        self.option_area.pack(fill=BOTH, expand=YES)
        
        list_area = LabelFrame(self.content_container)
        list_area.pack(side=BOTTOM, fill=BOTH, expand=YES)

        player_area = Frame(list_area)
        player_area.pack(side=LEFT)

        self.goal_area = GoalDisplay(list_area, manager)
        self.goal_area.pack(side=RIGHT)

        self.our_goals.trace("w", self.goal_area.handle_goals_update)
        if base_object is not None:
            self.goal_area.setup_from_object(base_object)

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

    def handle_venue_change(self, *args):
        """Called whenever the widget that selects venue is changed"""
        self.report.venue = self.selected_venue.get()
    
    def handle_match_type_change(self, *args):
        """Called whenever the widget that selects the match type is changed"""
        self.report.match_type = self.selected_match_type.get()

    def add_list(self, container, name, player_list: list[Player]):
        """Adds the given list of players to the screen in the container given."""
        name_frame = Frame(container)
        name_frame.pack(side=TOP)

        TableHeader(name_frame, text=name).pack(side=LEFT)
        Label(name_frame, text=len(player_list)).pack(side=LEFT)

        for player in player_list:
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

        self.add_list(self.starter_display, "FIRST XI", self.report.starting_lineup)
        self.add_list(self.sub_display, "SUBS", self.report.subs)
        self.goal_area.update_player_list(self.get_selected_players())

    def populate_player_list(self, initial_list, additive_list, player_list):
        for player_name in initial_list:
            player = self.club.get_player_by_name(player_name)
            if player is not None:
                additive_list.append(player)
                player_list.remove(player)

    def add_player_to_subs(self, player):
        """Adds the given player to the report's subs list"""
        if len(self.report.subs < MAX_SUBS):
            self.report.subs.append(player)
            self.available_players.remove(player)
            self.setup_player_lists()

    def add_player_to_starters(self, player):
        """Adds the given player to the reports starting_lineup"""
        if len(self.report.starting_lineup) < 11:
            self.self.report.starting_lineup.append(player)
            self.available_players.remove(player)
            self.setup_player_lists()

    def remove_player(self, player):
        """Removes the given player from whichever list they are currently selected in"""
        if player in self.report.starting_lineup:
            self.report.starting_lineup.remove(player)
        else:
            self.report.subs.remove(player)
        self.available_players.append(player)
        self.setup_player_lists()

    def setup_from_object(self, report: MatchReport):
        """Sets up the wizard from the given match report"""
        players = self.club.players[:]

        self.selected_opponent.set(report.opponent)
        self.selected_venue.set(str(report.venue))
        self.selected_match_type.set(str(report.match_type))
        self.selected_date = report.date

        self.populate_player_list(report.starting_lineup, self.report.starting_lineup, players)
        self.populate_player_list(report.subs, self.report.subs, players)
        self.available_players = players
        
        self.our_goals.set(report.club_goals)
        self.opponent_goals.set(report.opponent_goals)
        
    def add_opposition_list(self):
        if len(self.club.opponents) > 0:
            if self.opposition_list is not None:
                self.opposition_list.grid_forget()
            self.opposition_list = OptionMenu(self.option_area, self.selected_opponent, *list(self.club.opponents))
            self.opposition_list.grid(row=self.opponent_row, column=1)

    def add_opponent(self):
        """Adds an opponent to the list of possible opponents"""
        opponent_name = self.oppo_entry.get()
        if len(opponent_name) > 0:
            self.club.add_opponent(opponent_name)
            self.selected_opponent.set(opponent_name)

            self.add_opposition_list()
            while self.oppo_entry.get():
                self.oppo_entry.delete(0)

    def select_starter(self, player_id: str):
        """Called to add a player to the starting lineup"""
        if len(self.report.starting_lineup) < 11:
            self.move_player(self.available_players,
                             self.report.starting_lineup, player_id)

    def select_sub(self, player_id: str) -> None:
        """Called to add a player to the subs list"""
        if len(self.report.subs) < MAX_SUBS or Fixture.MatchType[self.selected_match_type.get()] == Fixture.MatchType.FRIENDLY:
            self.move_player(self.available_players, self.report.subs, player_id)
    
    def deselect_sub(self, player_id: str) -> None:
        """Called to remove a player from the subs list"""
        self.move_player(self.report.starting_lineup,
                         self.available_players, player_id)
        self.move_player(self.report.subs, self.available_players, player_id)
    
    def move_player(self, current_list, new_list, player_id: str):
        """Moves a player between two given lists"""
        if player_id in current_list:
            current_list.remove(player_id)
            new_list.append(player_id)
            new_list.sort()

            self.setup_objects_list()

    def setup_objects_list(self):
        self.setup_list(self.available_players_list, self.available_players, [ButtonInfo(self.select_sub, "SUB"), ButtonInfo(self.select_starter, "XI")]) 
        self.setup_list(self.selected_players_list, self.report.starting_lineup, [ButtonInfo(self.deselect_sub, "-")])
        self.setup_list(self.substitute_players_list, self.report.subs, [ButtonInfo(self.deselect_sub, "-")])
        self.goal_area.update_player_list(self.get_selected_players())
    
    def get_selected_players(self) -> list[str]:
        """Returns all the selected players"""
        return self.report.starting_lineup[:] + self.report.subs[:]

    def setup_list(self, player_display, players: list[Player], button_info_list):
        player_display.clear_widgets()

        widgets = []
        for player in players:
            entry_widget = PlayerEntry(list, object)

            for button_info in button_info_list:
                new_button = Button(entry_widget, text=button_info.icon, command=lambda w=player,
                                    button_action=button_info.action: button_action(w))
                entry_widget.add_control(new_button)
            widgets.append(entry_widget)
        player_display.setup(widgets)

    def handle_save_pressed(self):
        success, report = self.construct_report()
        if not success:
            return False, report

        self.club.remove_match_report(self.root_object)
        self.club.add_match_report(report)
        return True, ""

    def handle_add_pressed(self):
        """Called when the user presses add"""
        success, report = self.finalise_report()
        if not success:
            return False, report

        self.club.add_match_report(report)
        return True, report

    def finalise_report(self):
        """Validates the report before requesting to add it to the club"""
        new_report = MatchReport()

        if len(self.report.starting_lineup) != NUM_STARTERS:
            return False, "Not enough starters added to match report"
        if len(self.report.subs) > MAX_SUBS and new_report.match_type != MatchType.FRIENDLY:
            return False, "Too many players on subs bench"

        for sub in self.report.subs:
            new_report.add_sub(sub)
            
        new_report.club_name = self.club.short_name
        new_report.club_goals = self.our_goals.get()
        new_report.opponent_goals = self.opponent_goals.get()
        new_report.opponent = self.selected_opponent.get()
        new_report.date = self.date_entry.get_date()

        for goal in self.goal_area.goal_entries:
            new_goal = Goal(goal.goalscorer.get(), goal.assister.get(), "test goal description")
            new_report.add_goal(new_goal)

        return True, new_report