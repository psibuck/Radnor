from tkinter import Frame

from ui.widgets.goal_entry import GoalEntry
from ui.widgets.table import TableHeader

class GoalDisplay(Frame):

    def __init__(self, root, page_manager):
        super().__init__(root)

        self.root = page_manager.root
        TableHeader(self, text="Goals").grid(row=0, column=0)

        self.goal_entries: list[GoalEntry] = [] 
        self.player_list = []

    def update_player_list(self, list):
        self.player_list = list[:]
        for goal in self.goal_entries:
            goal.update_player_list(self.player_list)

    def handle_goals_update(self, var, _, a):
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