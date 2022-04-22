from ui.pages.page_base import PageBase
from ui.widgets.select_team_widget import SelectTeamWidget

class StatsPage(PageBase):
    
    def __init__(self, root, app):
        super().__init__(root, app)
        self.name = "stats"

    def SetupContent(self):
        self.ShowMatchReportList()

    def ShowMatchReportList(self):
        SelectTeamWidget(self.club.players, self)