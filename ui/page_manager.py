from enum import Enum

from ui.pages.club_selector import ClubSelector
from ui.pages.home import Home
from ui.pages.match_reports import MatchReports
from ui.pages.players import Players
from ui.pages.training_reports import TrainingReports

import tkinter as tk
from tkinter import ttk, BOTH, YES, IntVar, LEFT, LabelFrame, OptionMenu, TOP

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
WINDOW_MARGIN = 10

class ClubControls(Enum):
    CLUB_CONTROLS = 0
    SELECT_CLUB = 1
    EDIT_CLUB = 2
    DELETE_CLUB = 3
    
    def __str__(self):
        if self == ClubControls.CLUB_CONTROLS:
            return "Manage Club"
        elif self == ClubControls.DELETE_CLUB:
            return "Delete Club"
        elif self == ClubControls.EDIT_CLUB:
            return "Edit Club"
        elif self == ClubControls.SELECT_CLUB:
            return "Select Club"
        return self.name

class PageManager:

    def __init__(self, app):
        self.root = tk.Tk()

        self.app = app

        self.current_index = -1
        self.current_page = None
        
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_requested)
        self.root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

        self.app_frame = LabelFrame(self.root, height=WINDOW_HEIGHT - WINDOW_MARGIN, width=WINDOW_WIDTH - WINDOW_MARGIN)
        self.app_frame.pack(fill=BOTH, expand=YES)

        self.content_area = LabelFrame(self.app_frame)
        self.content_area.pack(side=TOP, fill=BOTH, expand=YES) 

        self.pages = [ClubSelector]
        self.switch_page(0)

    def handle_club_loaded(self):
        self.pages = []
        self.pages.append(Home)
        self.pages.append(Players)
        self.pages.append(MatchReports)
        self.pages.append(TrainingReports)
        self.root.title(self.app.club.name)
        self.setup_tabs()    
        self.switch_page(0)

    def get_screen_width(self):
        return WINDOW_WIDTH - 2 * WINDOW_MARGIN

    def get_screen_height(self):
        return WINDOW_HEIGHT - 2 * WINDOW_MARGIN
        
    def setup_tabs(self):
        frame = LabelFrame(self.app_frame, height=50)
        frame.pack(side=TOP)

        index = 0
        for page in self.pages:
            button = ttk.Button(frame, text = page.name, command = lambda index = index: self.switch_page(index))
            button.pack(side = LEFT)
            index += 1
        
        self.control = IntVar()
        self.control.set(ClubControls.CLUB_CONTROLS)
        OptionMenu(frame, self.control, *list(ClubControls), command=self.handle_control_selected).pack(side=LEFT)

    def handle_control_selected(self, value):
        if value == ClubControls.SELECT_CLUB:
            print("Select Club")
            self.open_club_selector()
        elif value == ClubControls.DELETE_CLUB:
            print("Delete Club")
            self.open_club_selector()

        if value != ClubControls.CLUB_CONTROLS:
            self.control.set(ClubControls.CLUB_CONTROLS)

    def open_club_selector(self):
        print("open club selector")

    def switch_page(self, page_index):
        if page_index < len(self.pages):
            
            if self.current_index == page_index:
                return
            
            self.current_index = page_index
            if self.current_page != None:
                self.current_page.shutdown()

            for widget in self.content_area.winfo_children():
                widget.destroy()

            self.open_page(self.pages[page_index])

    def open_page(self, page):
        self.current_page = page(self, self.content_area)
        self.current_page.setup_content()
        self.current_page.pack(fill=BOTH, expand=YES)

    def open_wizard(self, wizard_class, object=None):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.current_page = None
        
        new_page = wizard_class(self, self.content_area, object)
        new_page.pack(fill=BOTH, expand=YES)

    def on_wizard_closed(self):
        index_to_switch_to = self.current_index
        self.current_index = -1
        self.switch_page(index_to_switch_to)

    def draw(self):
        self.root.mainloop()

    def close_requested(self):
        self.app.quit()

    def shutdown(self):
        self.root.destroy()