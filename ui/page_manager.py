from re import I
from ui.pages.home import *
from ui.pages.match_reports import MatchReports
from ui.pages.training_reports import TrainingReports

import tkinter as tk
from tkinter import *


class PageManager:

    def __init__(self, app):
        self.root = tk.Tk()
        self.app = app

        self.current_index = 0
        self.current_page = None
        self.pages = []
        self.pages.append(HomePage)
        self.pages.append(MatchReports)
        self.pages.append(TrainingReports)
        self.root.geometry("800x600")
        self.root.title(self.app.club.name)
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
            
            self.current_index = page_index
            if self.current_page != None:
                self.current_page.Shutdown()

            for widget in self.content_area.winfo_children():
                widget.destroy()
 
            self.current_page = self.pages[page_index](self, self.content_area)
            self.current_page.SetupContent()
            self.current_page.pack(fill=BOTH)

    def OpenWizard(self, wizard_info):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.current_page = None
        
        new_page = wizard_info.wizard_class(self, self.content_area)
        new_page.pack(fill=BOTH)

    def OnWizardClosed(self):
        self.SwitchPage(self.current_index)

    def Draw(self):
        self.root.mainloop()

    def CloseRequested(self):
        self.app.Quit()

    def Shutdown(self):
        self.root.destroy()