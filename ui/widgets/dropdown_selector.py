"""File that contains dropdown selector class and associated helpers."""
from tkinter import Frame, OptionMenu, StringVar

class DropdownSelector(Frame):
    """A dropdown selector is a widget that takes a list of data and allows the user to select from it via a dropdown."""
    def __init__(self, root, selected_option, data_list, callback=None):
        super().__init__(root)
        self.menu = None
        self.variable = StringVar()
        self.variable.set(selected_option)
        self.set_list(data_list)
        self.callback = callback

    def set_list(self, data_list):
        if self.menu is not None:
            self.menu.pack_forget()
        if len(data_list) == 0:
            self.menu = OptionMenu(self, variable=self.variable, value="NONE", *data_list, command=self.handle_option_selected)
        else:
            self.menu = OptionMenu(self, self.variable, *data_list, command=self.handle_option_selected)
        self.menu.pack()

    def handle_option_selected(self, value):
        if self.callback != None:
            self.callback(value)