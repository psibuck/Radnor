from tkinter import Frame, Label, LEFT, OptionMenu, StringVar

import src.club.player as Player
from ui.widgets.dropdown_selector import DropdownSelector

DEFAULT_SELECTION_VALUE = "NONE"
class GoalEntry(Frame):

    def __init__(self, root, index, player_list):
        super().__init__(root)

        Label(self, text="Goal " + str(index)).pack(side=LEFT)
        self.dropdown_area = Frame(self)
        self.dropdown_area.pack(side = LEFT)
        
        self.goalscorer = StringVar()
        self.goalscorer.set(DEFAULT_SELECTION_VALUE)
        self.assister = StringVar()
        self.assister.set(DEFAULT_SELECTION_VALUE)

        self.update_player_list(player_list)


    def update_player_list(self, new_player_list: list[Player.Player]):
        self.player_list = []
        for player in new_player_list:
            self.player_list.append(player.get_name())

        self.update_display()

    def update_display(self):

        for widget in self.dropdown_area.winfo_children():
            widget.destroy()
        DropdownSelector(self.dropdown_area, self.goalscorer.get(), self.player_list[:], self.select_goalscorer).pack(side=LEFT)
        DropdownSelector(self.dropdown_area, self.assister.get(), self.player_list[:], self.select_assister).pack(side=LEFT)

    def _update_selected_value(self, stored_value, new_value):
        current_value = stored_value.get()
        if current_value != DEFAULT_SELECTION_VALUE:
            self.player_list.append(current_value)
            self.player_list.sort()

        stored_value.set(new_value)

    def _update_player_list(self, stored_value):
        stored = stored_value.get()
        if stored != DEFAULT_SELECTION_VALUE:
            if stored in self.player_list:
                self.player_list.remove(stored)
            else:
                stored_value.set(DEFAULT_SELECTION_VALUE)

    def select_goalscorer(self, value):
        self._update_selected_value(self.goalscorer, value)
        self._update_player_list(self.goalscorer)
        self.update_display()

    def select_assister(self, value):
        self._update_selected_value(self.assister, value)
        self._update_player_list(self.assister)
        self.update_display()

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