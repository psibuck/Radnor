from datetime import date
from tkinter import *
from src.match.fixture import MatchType, Venue
from src.match.goal import Goal
from src.match.match_report import MatchReport
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.date_entry import DateEntry
from ui.widgets.player_entry import PlayerEntry
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

class GoalEntry(Frame):

    def __init__(self, root, index, player_list):
        super().__init__(root)
        self.scorer_options = None
        self.assister_options = None
        self.player_list = []
        for player in player_list:
            self.player_list.append(player.get_name())

        Label(self, text="Goal " + str(index)).pack(side=LEFT)

        self.goalscorer = "None"
        self.assister = "None"
        self.goalscorer_var = StringVar()
        self.goalscorer_var.set("None")
        self.assister_var = StringVar() 
        self.assister_var.set("None")
        self.update_option_lists()

    def update_option_lists(self):
        lists = [self.scorer_options, self.assister_options]
        for i in range(len(lists)):
            list = lists[i]
            if list is not None:
                list.pack_forget()
            callback_function = None

            players = self.player_list[:] 
            if i == 1:
                if self.assister != "None":
                    players.append("None")

                callback_function = lambda variable: (self.handle_player_selected(variable, self.assister), self.set_assister(variable), self.update_option_lists())
                self.assister_options = OptionMenu(self, self.assister_var, *players, command=callback_function)
                self.assister_options.pack(side=LEFT)
            else:
                if self.goalscorer != "None":
                    players.append("None")
                callback_function = lambda variable: (self.handle_player_selected(variable, self.goalscorer), self.set_goalscorer(variable), self.update_option_lists())
                self.scorer_options = OptionMenu(self, self.goalscorer_var, *players, command=callback_function)
                self.scorer_options.pack(side=LEFT)

    def set_goalscorer(self, name):
        self.goalscorer = name

    def set_assister(self, name):
        self.assister = name

    def handle_player_selected(self, selected_player, current_player):
        if current_player != "None":
            self.player_list.append(current_player)
            self.player_list.sort()

        if selected_player != "None":
            self.player_list.remove(selected_player)

class GoalDisplay(Frame):

    def __init__(self, root, page_manager):
        super().__init__(root)

        self.root = page_manager.root
        TableHeader(self, text="Goals").grid(row=0, column=0)

        self.goal_entries = []

    def update_player_list(self, list):
        self.player_list = list

    def handle_goals_update(self, var, index, mode):
        raw_goals = self.root.globalgetvar(var)
        if raw_goals != "":
            num_goals = int(raw_goals)
            current_goals = len(self.goal_entries)
            entry_discrepancy = current_goals - num_goals
            if entry_discrepancy > 0:
                for _ in range(entry_discrepancy):
                    entry = self.goal_entries[-1]
                    entry.grid_forget()
                    self.goal_entries.remove(entry)
            elif entry_discrepancy < 0:
                for i in range(current_goals, num_goals):
                    new_entry = GoalEntry(self, i + 1, self.player_list)
                    new_entry.grid(row=i, column=0)
                    self.goal_entries.append(new_entry)


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

        self.available_players = manager.app.club.players
        self.first_XI = []
        self.subs = []

        self.selected_opponent = StringVar()
        self.selected_venue = StringVar()
        self.selected_venue.set(str(Venue(1)))

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
        self.goal_area.update_player_list(self.available_players)

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
        self.selected_match_type = StringVar()
        self.selected_match_type.set(str(MatchType(1)))
        match_type_selector = OptionMenu(self.option_area, self.selected_match_type, *list(MatchType))
        match_type_selector.grid(row=self.match_type_row, column=1)

        TableHeader(self.option_area, "Venue").grid(row=self.venue_row, column=0)
        venue_selector = OptionMenu(self.option_area, self.selected_venue, *list(Venue))
        venue_selector.grid(row=self.venue_row, column=1)

        self.date_entry = DateEntry(self.option_area, default_year = date.today().year, years_to_show=2)
        self.date_entry.grid(row=self.date_row, column=0, columnspan=5)

        self.available_players_list = ObjectListWidget(player_area, "Available Players")
        self.available_players_list.grid(row=1, column=0, sticky=N)

        self.selected_players_list = ObjectListWidget(player_area, "First XI")
        self.selected_players_list.grid(row=1, column=1, sticky=N)

        self.substitute_players_list = ObjectListWidget(player_area, "Substitutes")
        self.substitute_players_list.grid(row=1, column=2, sticky=N)
                
        self.setup_objects_list()

    def populate_player_list(self, initial_list, additive_list, player_list):
        for player_name in initial_list:
            player = self.club.get_player_by_name(player_name)
            if player != None:
                additive_list.append(player)
                player_list.remove(player)

    def setup_from_object(self, object):
        players = self.club.players[:]

        self.populate_player_list(object.starting_lineup, self.first_XI, players)
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
        if len(self.first_XI) != NUM_STARTERS:
            return False, "Not enough starters added to match report"
        if len(self.subs) > MAX_SUBS:
            return False, "Too many players on subs bench"

        for player in self.first_XI:
            self.report.add_starter(player)
        for sub in self.subs:
            self.report.add_sub(sub)
            
        self.report.club_goals = self.our_goals.get()
        self.report.opponent_goals = self.opponent_goals.get()
        self.report.match_type = MatchType[self.selected_match_type.get()]
        self.report.venue = Venue[self.selected_venue.get()]
        self.report.opponent = self.selected_opponent.get()
        self.report.date = self.date_entry.get_date()

        for goal in self.goal_area.goal_entries:
            new_goal = Goal(goal.goalscorer, goal.assister, "test goal description")
            self.report.add_goal(new_goal)

        self.club.add_match_report(self.report)
        self.close()    
        return True, ""    