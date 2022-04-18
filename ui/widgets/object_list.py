from tkinter import *

class ObjectListWidget(Frame):

    def __init__(self, parent, title = ""):
        Frame.__init__(self, parent)
        self.title = title
        self.title_label = None

    def Setup(self, widgets):
        if self.title != "" and self.title_label == None:
            self.title_label = Label(self, text = self.title)
            self.title_label.pack(side=TOP)

        for widget in widgets:
            widget.pack(side=TOP)

    def ClearWidgets(self):
        for widget in self.winfo_children():
            if widget is not self.title_label:
                widget.destroy()


