from ui.pages.home import *
from ui.pages.player_finances import FinancesPage
from ui.pages.player_stats import StatsPage

import tkinter as tk
from tkinter import *

class PageManager:

    def __init__(self, app):
        self.page_index = 0
        self.pages = []
        self.pages.append(HomePage(self))
        self.pages.append(StatsPage(self))
        self.pages.append(FinancesPage(self))
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Club Name Here")
        self.root.protocol("WM_DELETE_WINDOW", self.CloseRequested)
        self.app = app

        self.SetupTabs()

        self.content_area = tk.Frame(self.root)
        self.content_area.pack(fill=BOTH, expand=YES)
        
        button = Button(self.content_area, text = "test")
        button.pack(fill=BOTH, expand = YES)
        self.SwitchPage(self.page_index)

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
            self.page_index = page_index
        
        for widget in self.content_area.winfo_children():
            widget.destroy()

        page = self.pages[self.page_index]
        page.SetupContent(self.content_area)

    def Draw(self):
        self.root.mainloop()

    def CloseRequested(self):
        self.app.Quit()

    def Shutdown(self):
        self.root.destroy()