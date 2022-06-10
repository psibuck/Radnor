from ui.pages.home import Home
from ui.pages.match_reports import MatchReports
from ui.pages.players import Players
from ui.pages.training_reports import TrainingReports

import tkinter as tk
from tkinter import ttk, BOTH, YES, Button, LEFT, LabelFrame,TOP

WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
WINDOW_MARGIN = 10

class PageManager:

    def __init__(self, app):
        self.root = tk.Tk()

        self.app = app

        self.current_index = -1
        self.current_page = None
        self.pages = []
        self.pages.append(Home)
        self.pages.append(Players)
        self.pages.append(MatchReports)
        self.pages.append(TrainingReports)
        self.root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.root.title(self.app.club.name)
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.close_requested)

        self.app_frame = LabelFrame(self.root, height=WINDOW_HEIGHT - WINDOW_MARGIN, width=WINDOW_WIDTH - WINDOW_MARGIN)
        self.app_frame.pack(fill=BOTH, expand=YES)

        self.setup_tabs()  
        self.content_area = LabelFrame(self.app_frame)
        self.content_area.pack(side=TOP, fill=BOTH, expand=YES)      
        self.switch_page(0)

    def get_screen_width(self):
        return WINDOW_WIDTH - 2 * WINDOW_MARGIN

    def get_screen_height(self):
        return WINDOW_HEIGHT - 2 * WINDOW_MARGIN
        
    def setup_tabs(self):
        frame = LabelFrame(self.app_frame, height=50)
        frame.pack()

        index = 0
        for page in self.pages:
            button = ttk.Button(frame, text = page.name, command = lambda index = index: self.switch_page(index))
            button.pack(side = LEFT)
            index += 1
        Button(frame, text="Clear Local Data", command=self.app.clear_local_data).pack(side=LEFT)

    def switch_page(self, page_index):
        if page_index < len(self.pages):
            
            if self.current_index == page_index:
                return
            
            self.current_index = page_index
            if self.current_page != None:
                self.current_page.shutdown()

            for widget in self.content_area.winfo_children():
                widget.destroy()

            self.current_page = self.pages[page_index](self, self.content_area)
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