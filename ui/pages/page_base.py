from tkinter import Label

class PageBase:

    def __init__(self, manager):
        self.manager = manager

    def SetupContent(self, frame):
        label = Label(frame, text="unimplemented page")
        label.pack()
        return 

    def Shutdown(self):
        return