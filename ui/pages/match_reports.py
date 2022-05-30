from tkinter import Button, Frame, LEFT, RIGHT, BOTTOM, TOP

from ui.pages.page_base import PageBase
from ui.widgets.table import Table, TableColumn
from ui.widgets.labels import Title
from ui.wizards.create_match_report_wizard import CreateMatchReportWizard
from ui.wizards.wizard_base import WizardInfo

class MatchReports(PageBase):
    name = "Matches"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.name = "Matches"
        Button(self, text="Add Fixture", command=self.HandleCreateFixturePressed).pack(side=TOP)
        Button(self, text="Add Result", command=self.HandleCreateResultPressed).pack(side=TOP)
        self.match_report_widget = None

    def SetupContent(self):
        self.fixture_space = Frame(self)
        self.fixture_space.pack(side = LEFT)
        self.match_report_space = Frame(self)
        self.match_report_space.pack(side = RIGHT)
        
        self.ShowFixtureList()
        self.ShowMatchReportList()

    def ShowFixtureList(self):
        for widget in self.fixture_space.winfo_children():
            widget.destroy()

        Title(self.fixture_space, "Fixtures").pack(side = TOP)
        fixture_table = Table(self.fixture_space, remove_func=self.HandleRemoveFixture)
        fixture_table.pack(side = TOP)  

        columns = [TableColumn("Date", function="GetDate"), TableColumn("Vs", "opponent"), TableColumn("Type", function="GetMatchType")]
        fixture_table.AddColumns(columns)
        for fixture in self.club.fixtures:
            fixture_table.AddObject(fixture)

    def ShowMatchReportList(self):
        for widget in self.match_report_space.winfo_children():
            widget.destroy()

        Title(self.match_report_space, "Results").pack(side = TOP)
        report_table = Table(self.match_report_space, remove_func=self.HandleRemoveMatchReport)
        report_table.pack(side = TOP)

        columns = [TableColumn("Date", function="GetDate"), TableColumn("Scoreline", function="GetScoreline"), TableColumn("Type", function="GetMatchType")]
        report_table.AddColumns(columns)
        for match_report in self.club.match_reports:
            report_table.AddObject(match_report)

    def HandleRemoveMatchReport(self, report):
        self.club.RemoveMatchReport(report)
        self.ShowMatchReportList()

    def HandleRemoveFixture(self, fixture):
        return
    
    def HandleCreateResultPressed(self):   
        self.page_manager.OpenWizard(WizardInfo(CreateMatchReportWizard))

    def HandleCreateFixturePressed(self):
        return

    def ShutDown(self):
        self.pending_report = None
