from tkinter import *
import tkinter as tk 

from ui.pages.page_base import PageBase
from ui.widgets.table import Table, TableColumn
from ui.widgets.scrollframe import ScrollFrame

class Home(PageBase):
    name = "Club"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)

    def setup_content(self):
        screen_width = self.page_manager.get_window_width()
        num_tables = 3
        box_width = screen_width / num_tables

        fixture_info = ScrollFrame(self, width = box_width)
        fixture_info.pack(side=LEFT, anchor=N, padx=5, fill=Y)
        fixture_table = Table(fixture_info.content_area)
        fixture_table.pack(side = TOP)  

        columns = [TableColumn("Date", function="get_date"), TableColumn("Vs", "opponent"), TableColumn("Type", function="get_match_type")]
        fixture_table.add_columns(columns)
        for fixture in self.club.fixtures:
            fixture_table.add_object(fixture)

        results_info = ScrollFrame(self, width = box_width)
        results_info.pack(side=LEFT, anchor=N, padx=5)
        results_table = Table(results_info.content_area)
        results_table.pack(side = TOP)  
        columns = [TableColumn("Date", function="get_date"), TableColumn("Scoreline", function="get_scoreline"), TableColumn("Type", function="get_match_type")]
        results_table.add_columns(columns)
        for match_report in self.club.match_reports:
            results_table.add_object(match_report)

        top_scorers = ScrollFrame(self, width = box_width)
        top_scorers.pack(side=LEFT, anchor=N, padx=5)
        top_scorers_table = Table(top_scorers.content_area)
        top_scorers_table.pack(side = TOP)  
        columns = [TableColumn("Name", function="get_name"), TableColumn("Goals", "goals")]
        top_scorers_table.add_columns(columns)
        top_scorers = self.club.get_top_scorers(5)
        for player in top_scorers:
            top_scorers_table.add_object(player)

        