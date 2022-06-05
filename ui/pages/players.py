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
        self.player_list = Table(self, remove_func=self.on_remove_player_button_pressed)
        columns = [TableColumn("Name", function="get_name"), TableColumn("DOB", "dob"), TableColumn("Appearances", function = "get_appearances"), TableColumn("Training", "training_attendance")]
        self.player_list.add_columns(columns)
        self.player_list.pack(side=LEFT)
        
        self.refresh_player_list()

    def refresh_player_list(self):
        self.player_list.clear_rows()

        for player in self.club.players:
            self.player_list.add_object(player)    

    def on_add_player_button_pressed(self):
        self.page_manager.open_wizard(AddPlayerWizard)

    def on_remove_player_button_pressed(self, player):
        self.club.remove_player(player)
        self.refresh_player_list()