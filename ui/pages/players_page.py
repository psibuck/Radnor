from tkinter import *
from ui.pages.page_base import PageBase
from ui.pages.player_info_page import PlayerView
from ui.widgets.scrollframe import ScrollFrame
from ui.widgets.table import Table, TableColumn
from ui.wizards.add_player_wizard import AddPlayerWizard

class Players(PageBase):
    name = "Players"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        
    def setup_content(self):
        Button(self, text="Add Player", command=self.on_add_player_button_pressed).pack(side=BOTTOM)
        self.show_player_list()

    def show_player_list(self):
        scroll_box = ScrollFrame(self)
        scroll_box.pack(fill=BOTH, expand=YES)
        self.player_list = Table(scroll_box.content_area, select_func=self.on_edit_player_selected, view_func=self.on_view_player_selected)
        columns = [TableColumn("Name", function="get_name"), TableColumn("DOB", "dob"),\
                   TableColumn("Appearances", function = "get_appearances"), \
                   TableColumn("Training", "training_attendance"), \
                   TableColumn("Signed On", function="get_is_signed_on"), TableColumn("Goals", "goals"), \
                   TableColumn("Assists", "assists")]
        self.player_list.add_columns(columns)
        self.player_list.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        self.refresh_player_list()

    def refresh_player_list(self):
        self.player_list.clear_rows()

        for player in self.club.players:
            self.player_list.add_object(player)    

    def on_add_player_button_pressed(self):
        self.page_manager.open_subpage(AddPlayerWizard)

    def on_edit_player_selected(self, player):
        self.page_manager.open_subpage(AddPlayerWizard, player)

    def on_view_player_selected(self, player):
        self.page_manager.open_subpage(PlayerView, player)