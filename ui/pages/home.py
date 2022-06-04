from tkinter import LEFT

from ui.pages.page_base import PageBase
from ui.widgets.table import Table, TableColumn

class Home(PageBase):
    name = "Club"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)

    def setup_content(self):
        fixture_table = Table(self)
        fixture_table.pack(side = LEFT)  

        columns = [TableColumn("Date", function="get_date"), TableColumn("Vs", "opponent"), TableColumn("Type", function="get_match_type")]
        fixture_table.add_columns(columns)
        for fixture in self.club.fixtures:
            fixture_table.add_object(fixture)

        results_table = Table(self)
        results_table.pack(side = LEFT)
        columns = [TableColumn("Date", function="get_date"), TableColumn("Scoreline", function="get_scoreline"), TableColumn("Type", function="get_match_type")]
        results_table.add_columns(columns)
        for match_report in self.club.match_reports:
            results_table.add_object(match_report)

        