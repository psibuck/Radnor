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
        self.root.protocol("WM_DELETE_WINDOW", self.close_requested)

        self.setup_tabs()  
        self.content_area = tk.Frame(self.root)
        self.content_area.pack(fill=BOTH, expand=YES)      
        self.switch_page(0)

    def setup_tabs(self):
        frame = tk.Frame(self.root, height=50)
        frame.pack()

        index = 0
        for page in self.pages:
            button = Button(frame, text = page.name, command = lambda index = index: self.switch_page(index))
            button.pack(side = LEFT)
            index += 1

    def switch_page(self, page_index):
        if page_index < len(self.pages):
            
            self.current_index = page_index
            if self.current_page != None:
                self.current_page.shutdown()

            for widget in self.content_area.winfo_children():
                widget.destroy()
 
            self.current_page = self.pages[page_index](self, self.content_area)
            self.current_page.setup_content()
            self.current_page.pack(fill=BOTH)

    def open_wizard(self, wizard_info):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.current_page = None
        
        new_page = wizard_info.wizard_class(self, self.content_area)
        new_page.pack(fill=BOTH)

    def on_wizard_closed(self):
        self.switch_page(self.current_index)

    def draw(self):
        self.root.mainloop()

    def close_requested(self):
        self.app.quit()

    def shutdown(self):
        self.root.destroy()