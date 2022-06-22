from tkinter import Frame, OptionMenu, StringVar

class DropdownSelector(Frame):

    def __init__(self, root, list, callback=None):
        super().__init__(root)
        self.menu = None
        self.selected_option = StringVar()
        self.selected_option.set("None")
        self.set_list(list)
        self.callback = callback

    def set_list(self, list):
        if self.menu != None:
            self.menu.pack_forget()
        self.menu = OptionMenu(self, self.selected_option, *list, command=self.handle_option_selected)
        self.menu.pack()

    def handle_option_selected(self, value):
        if self.callback != None:
            self.callback(value)