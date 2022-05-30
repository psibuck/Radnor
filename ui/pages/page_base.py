from tkinter import Label
from tkinter import Frame

class PageBase(Frame):
    name = "No name provided"
    
    def __init__(self, manager, root):
        Frame.__init__(self, root)
        self.page_manager = manager
        self.root = root
        self.club = manager.app.club

    def SetupContent(self):
        label = Label(self, text="unimplemented page")
        label.pack()
        return 

    def Shutdown(self):
        for widget in self.winfo_children():
            widget.destroy()