from ui.pages.page_base import PageBase
from ui.widgets.create_match_report_widget import CreateMatchReportWidget

class StatsPage(PageBase):
    
    def __init__(self, root, app):
        super().__init__(root, app)
        self.name = "stats"

    def SetupContent(self):
        self.ShowMatchReportList()

    def ShowMatchReportList(self):
        CreateMatchReportWidget(self.club.players, self)