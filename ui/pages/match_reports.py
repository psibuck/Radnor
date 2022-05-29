from src.match.match_report import MatchReport

from ui.pages.page_base import PageBase
from ui.widgets.create_match_report_widget import CreateMatchReportWidget
from ui.widgets.table import Table, TableColumn
from tkinter import Button, Frame, Label, BOTTOM, TOP

class MatchReports(PageBase):
    name = "Matches"
    
    def __init__(self, root, app):
        super().__init__(root, app)
        self.name = "Matches"
        self.save_button = None
        self.add_button = None
        self.match_report_widget = None

    def SetupContent(self):
        self.save_button = Button(self, text = "Save", command = self.HandleSaveClicked)
        self.match_report_space = Frame(self)
        self.match_report_space.pack(side = TOP)

        self.ShowMatchReportList()
        button = Button(self, text="+", command=self.HandleAddButtonPressed)
        button.pack(side = BOTTOM)

    def ShowMatchReportList(self):
        for widget in self.match_report_space.winfo_children():
            widget.destroy()

        report_table = Table(self.match_report_space, remove_func=self.HandleRemoveMatchReport)
        report_table.pack(side = TOP)

        columns = [TableColumn("Date", function="GetDate"), TableColumn("Scoreline", function="GetScoreline"), TableColumn("Type", function="GetMatchType")]
        report_table.AddColumns(columns)
        for match_report in self.club.match_reports:
            report_table.AddObject(match_report)

    def HandleRemoveMatchReport(self, report):
        self.club.RemoveMatchReport(report)
        self.ShowMatchReportList()

    def HandleSaveClicked(self):
        self.save_button.pack_forget()
        self.club.AddMatchReport(self.match_report_widget.CreateMatchReport())
        self.ShowMatchReportList()
    
    def HandleAddButtonPressed(self):   
        self.match_report_widget = CreateMatchReportWidget(self.club, self.match_report_space)
        self.save_button.pack(side = BOTTOM)

    def ShutDown(self):
        self.pending_report = None
