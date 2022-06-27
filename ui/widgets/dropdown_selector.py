from tkinter import Frame, OptionMenu, StringVar

class DropdownSelector(Frame):

    def __init__(self, root, selected_option, list, callback=None):
        super().__init__(root)
        self.menu = None
        self.variable = StringVar()
        self.variable.set(selected_option)
        self.set_list(list)
        self.callback = callback

    def set_list(self, list):
        if self.menu != None:
            self.menu.pack_forget()
        self.menu = OptionMenu(self, self.variable, *list, command=self.handle_option_selected)
        self.menu.pack()

    def handle_option_selected(self, value):
        if self.callback != None:
            self.callback(value)