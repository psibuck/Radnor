from re import I
from ui.pages.home import *
from ui.pages.player_finances import FinancesPage
from ui.pages.player_stats import StatsPage
from ui.pages.match_reports import MatchReports
from ui.pages.training_reports import TrainingReports

import tkinter as tk
from tkinter import *


class PageManager:

    def __init__(self, app):
        self.root = tk.Tk()
        self.app = app

        self.current_page = None
        self.pages = []
        self.pages.append(HomePage)
        self.pages.append(MatchReports)
        self.pages.append(TrainingReports)
        self.root.geometry("800x600")
        self.root.title("Club Name Here")
        self.root.protocol("WM_DELETE_WINDOW", self.CloseRequested)

        self.SetupTabs()  
        self.content_area = tk.Frame(self.root)
        self.content_area.pack(fill=BOTH, expand=YES)      
        self.SwitchPage(0)

    def SetupTabs(self):
        frame = tk.Frame(self.root, height=50)
        frame.pack()

        index = 0
        for page in self.pages:
            button = Button(frame, text = page.name, command = lambda index = index: self.SwitchPage(index))
            button.pack(side = LEFT)
            index += 1

    def SwitchPage(self, page_index):
        if page_index < len(self.pages):
        
            if self.current_page != None:
                self.current_page.Shutdown()

            for widget in self.content_area.winfo_children():
                widget.destroy()
 
            self.current_page = self.pages[page_index](self.content_area, self.app)
            self.current_page.SetupContent()
            self.current_page.pack(fill=BOTH)

    def Draw(self):
        self.root.mainloop()

    def CloseRequested(self):
        self.app.Quit()

    def Shutdown(self):
        self.root.destroy()