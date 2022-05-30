from tkinter import *

class ObjectListWidget(Frame):

    def __init__(self, parent, title = ""):
        Frame.__init__(self, parent)
        self.title = title
        self.title_label = None

    def setup(self, widgets):
        if self.title != "" and self.title_label == None:
            self.title_label = Label(self, text = self.title)
            self.title_label.grid(column=0, row=0)

        row = 1
        for widget in widgets:
            widget.grid(column=0, row=row)
            row += 1

    def clear_widgets(self):
        for widget in self.winfo_children():
            if widget is not self.title_label:
                widget.destroy()