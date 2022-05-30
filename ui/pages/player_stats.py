from ui.pages.page_base import PageBase
from ui.wizards.create_match_report_wizard import CreateMatchReportWidget

class StatsPage(PageBase):
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.name = "stats"

    def SetupContent(self):
        self.ShowMatchReportList()

    def ShowMatchReportList(self):
        CreateMatchReportWidget(self.club, self)