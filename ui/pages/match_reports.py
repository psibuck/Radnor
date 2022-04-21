from difflib import Match
from src.match.match_report import MatchReport

from ui.pages.page_base import PageBase
from ui.widgets.select_team_widget import SelectTeamWidget
from tkinter import Button, Frame, Label, BOTTOM, TOP

class MatchReports(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "Matches"
        self.frame = None
        self.save_button =  None
        self.match_report_widget = None

    def SetupContent(self, frame):
        if self.frame == None:
            self.frame = frame
        self.save_button = Button(self.frame, text = "Save", command = self.HandleSaveClicked)
        self.add_button = Button(self.frame, text = "+", command = self.HandleAddButtonPressed)
        self.match_report_space = Frame(self.frame)
        self.match_report_space.pack(side = TOP)

        self.ShowMatchReportList()

    def ShowMatchReportList(self):
        count = 0
        for match_report in self.manager.app.club.match_reports:
            label = Label(self.frame, text = match_report.subs[0])
            #label.grid(row=count, column=1)
            label.pack()
            count += 1
        self.add_button.pack(side = TOP)

    def HandleSaveClicked(self):
        self.save_button.pack_forget()
        self.add_button.pack(side = BOTTOM)

        new_report = MatchReport()
        for player in self.match_report_widget.first_XI:
            new_report.AddStarter(player)
        for sub in self.match_report_widget.subs:
            new_report.AddSub(sub)
        self.manager.app.club.match_reports.append(new_report)

        for widget in self.match_report_space.winfo_children():
            widget.destroy()

        self.ShowMatchReportList()

    
    def HandleAddButtonPressed(self):   
        self.match_report_widget = SelectTeamWidget(self.manager.app.club.players, self.match_report_space)
        self.save_button.pack(side = BOTTOM)
        self.add_button.pack_forget()


    def ShutDown(self):
        self.pending_report = None
