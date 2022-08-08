from tkinter import Label
from tkinter import Frame

import src.club.club as Club

class PageBase(Frame):
    name = "No name provided"
    
    def __init__(self, manager, root):
        Frame.__init__(self, root)
        self.page_manager = manager
        self.root = root
        self.club: Club.Club = manager.club

    def setup_content(self):
        label = Label(self, text="unimplemented page")
        label.pack()
        return 

    def shutdown(self):
        for widget in self.winfo_children():
            widget.destroy()

    def close(self):
        self.page_manager.on_page_closed()