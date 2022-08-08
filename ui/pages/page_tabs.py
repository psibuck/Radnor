import ui.pages.page_base as PB

from ui.pages.home import Home
from ui.pages.match_reports import MatchReports
from ui.pages.players_page import Players
from ui.pages.training_reports import TrainingReports

PAGE_TABS: list[PB.PageBase] = [
    Home,
    Players,
    MatchReports,
    TrainingReports
]