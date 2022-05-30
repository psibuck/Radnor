from ui.pages.page_base import PageBase

class StatsPage(PageBase):
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        self.name = "stats"

    def setup_content(self):
        self.show_match_report_list()