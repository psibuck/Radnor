from enum import Enum

import src.application as Application
from src.club.club import Club
from ui.pages.page_tabs import PAGE_TABS
from ui.pages.club_selector import ClubSelector

import tkinter as tk
from tkinter import ttk, BOTH, YES, IntVar, LEFT, LabelFrame, OptionMenu, TOP

import os
from PIL import Image, ImageTk

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
    """The page manager is the controller for the UI. It opens pages, handles closing and listens for global user input."""
    def __init__(self, app: Application.Application):
        self.root = tk.Tk()

        self.app: Application.Application = app
        self.app.on_club_loaded = self.handle_club_loaded
        self.app.on_application_shutdown = self.shutdown
        
        self.club: Club = app.club
        self.current_index = -1
        self.current_page = None
        
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_requested)
        self.root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

        ico = Image.open(os.getcwd() + "/data/graphics/radnor_logo.png")
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

        self.app_frame = LabelFrame(self.root, height=WINDOW_HEIGHT - WINDOW_MARGIN, width=WINDOW_WIDTH - WINDOW_MARGIN)
        self.app_frame.pack(fill=BOTH, expand=YES)

        self.content_area = LabelFrame(self.app_frame)
        self.content_area.pack(side=TOP, fill=BOTH, expand=YES) 
        
        self.tab_frame = LabelFrame(self.app_frame, height=50)
        self.open_club_selector()

    def handle_club_loaded(self, club: Club):
        self.club = club

        self.pages: list[__class__] = PAGE_TABS

        self.content_area.pack_forget()
        self.setup_tabs() 
        self.content_area.pack(side=TOP, fill=BOTH, expand=YES) 

        self.current_index = -1   
        self.switch_page(0)

        self.root.title(self.club.name)

    def get_window_width(self):
        """Returns the width of the window."""
        return WINDOW_WIDTH - 2 * WINDOW_MARGIN

    def get_window_height(self):
        """Returns the height of the window."""
        return WINDOW_HEIGHT - 2 * WINDOW_MARGIN
        
    def setup_tabs(self):
        for widget in self.tab_frame.winfo_children():
            widget.destroy()

        self.tab_frame.pack(side=TOP)

        index = 0
        for page in self.pages:
            button = ttk.Button(self.tab_frame, text = page.name, command = lambda index = index: self.switch_page(index))
            button.pack(side = LEFT)
            index += 1
        
        self.control = IntVar()
        self.control.set(ClubControls.CLUB_CONTROLS)
        OptionMenu(self.tab_frame, self.control, *list(ClubControls), command=self.handle_control_selected).pack(side=LEFT)

    def handle_control_selected(self, value):
        if value == ClubControls.SELECT_CLUB:
            self.open_club_selector()
        elif value == ClubControls.DELETE_CLUB:
            self.app.remove_club(self.app.club)
            self.open_club_selector()
           
        if value != ClubControls.CLUB_CONTROLS:
            self.control.set(ClubControls.CLUB_CONTROLS)

    def open_club_selector(self):
        self.root.title("Select Club")
        self.pages = [ClubSelector]
        self.tab_frame.pack_forget()
        self.current_index = -1
        self.switch_page(0)
        
    def close_current_page(self):
        if self.current_page != None:
            self.current_page.shutdown()
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def switch_page(self, page_index):
        if page_index < len(self.pages):
            
            if self.current_index == page_index:
                return
            
            self.current_index = page_index

            self.close_current_page()

            self.open_page(self.pages[page_index])

    def open_page(self, page):
        self.current_page = page(self, self.content_area)
        self.current_page.setup_content()
        self.current_page.pack(fill=BOTH, expand=YES)

    def open_subpage(self, page_class, object=None):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        self.current_page = None
        
        new_page = page_class(self, self.content_area, object)
        new_page.pack(fill=BOTH, expand=YES)

    def on_page_closed(self):
        index_to_switch_to = self.current_index
        self.current_index = -1
        self.switch_page(index_to_switch_to)

    def draw(self):
        self.root.mainloop()

    def close_requested(self):
        self.app.quit()

    def shutdown(self):
        self.root.destroy()