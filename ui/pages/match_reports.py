from tkinter import Button, Frame, LEFT, RIGHT, BOTTOM, TOP

from ui.pages.page_base import PageBase
from ui.widgets.table import Table, TableColumn
from ui.widgets.labels import Title
from ui.wizards.add_fixture_wizard import AddFixtureWizard
from ui.wizards.add_match_report_wizard import AddMatchReportWizard

class MatchReports(PageBase):
    name = "Matches"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.name = "Matches"
        Button(self, text="Add Fixture", command=self.handle_create_fixture_pressed).pack(side=TOP)
        Button(self, text="Add Result", command=self.handle_create_result_pressed).pack(side=TOP)
        self.match_report_widget = None

    def setup_content(self):
        self.fixture_space = Frame(self)
        self.fixture_space.pack(side = LEFT)
        self.match_report_space = Frame(self)
        self.match_report_space.pack(side = RIGHT)
        
        self.show_fixture_list()
        self.show_match_report_list()

    def show_fixture_list(self):
        for widget in self.fixture_space.winfo_children():
            widget.destroy()

        Title(self.fixture_space, "Fixtures").pack(side = TOP)
        fixture_table = Table(self.fixture_space, remove_func=self.handle_remove_fixture)
        fixture_table.pack(side = TOP)  

        columns = [TableColumn("Date", function="get_date"), TableColumn("Vs", "opponent"), TableColumn("Type", function="get_match_type")]
        fixture_table.add_columns(columns)
        for fixture in self.club.fixtures:
            fixture_table.add_object(fixture)

    def show_match_report_list(self):
        for widget in self.match_report_space.winfo_children():
            widget.destroy()

        Title(self.match_report_space, "Results").pack(side = TOP)
        report_table = Table(self.match_report_space, remove_func=self.handle_remove_match_report)
        report_table.pack(side = TOP)

        columns = [TableColumn("Date", function="get_date"), TableColumn("Scoreline", function="get_scoreline"), TableColumn("Type", function="get_match_type")]
        report_table.add_columns(columns)
        for match_report in self.club.match_reports:
            report_table.add_object(match_report)

    def handle_remove_match_report(self, report):
        self.club.remove_match_report(report)
        self.show_match_report_list()

    def handle_remove_fixture(self, fixture):
        return
    
    def handle_create_result_pressed(self):  
        self.page_manager.open_wizard(AddMatchReportWizard)

    def handle_create_fixture_pressed(self):
        self.page_manager.open_wizard(AddFixtureWizard)

    def shutdown(self):
        self.pending_report = None
