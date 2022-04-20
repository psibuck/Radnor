from ui.pages.page_base import PageBase
from ui.widgets.select_team_widget import SelectTeamWidget

class StatsPage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "stats"
        self.frame = None

    def SetupContent(self, frame):
        if self.frame == None:
            self.frame = frame

        self.ShowMatchReportList()

    def ShowMatchReportList(self):
        SelectTeamWidget(self.manager.app.club.players, self.frame)
