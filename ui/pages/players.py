from select import select
from tkinter import *
from ui.pages.page_base import PageBase
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
        self.player_list = Table(self, select_func=self.on_edit_player_selected)
        columns = [TableColumn("Name", function="get_name"), TableColumn("DOB", "dob"), TableColumn("Appearances", function = "get_appearances"), TableColumn("Training", "training_attendance"), TableColumn("Signed On", function="get_is_signed_on")]
        self.player_list.add_columns(columns)
        self.player_list.pack(side=TOP)
        
        self.refresh_player_list()

    def refresh_player_list(self):
        self.player_list.clear_rows()

        for player in self.club.players:
            self.player_list.add_object(player)    

    def on_add_player_button_pressed(self):
        self.page_manager.open_wizard(AddPlayerWizard)

    def on_edit_player_selected(self, player):
        self.page_manager.open_wizard(AddPlayerWizard, player)