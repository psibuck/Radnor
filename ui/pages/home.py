from tkinter import *
from ui.pages.page_base import PageBase
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.player_entry import PlayerEntry
from ui.widgets.table import Table, TableColumn

class HomePage(PageBase):
    name = "Club"
    
    def __init__(self, root, app):
        super().__init__(root, app)

        self.input_box = None
        self.player_list = None
        
    def SetupContent(self):
        self.ShowPlayerButtonArea()
        self.ShowPlayerList()

    def ShowPlayerList(self):
        self.player_list = ObjectListWidget(self, "Player List")
        self.player_list.pack(side=TOP)
        
        self.RefreshPlayerList()

    def RefreshPlayerList(self):
        self.player_list.ClearWidgets()

        player_table = Table(self.player_list, remove_func=self.OnRemovePlayerButtonPressed)
        columns = [TableColumn("Name", "name"), TableColumn("Appearances", function = "GetAppearances"), TableColumn("Training", "training_attendance")]
        player_table.AddColumns(columns)
        for player in self.club.players:
            player_table.AddObject(player)

        player_table.pack(side=TOP)
        
    def ShowPlayerButtonArea(self):
        add_player_frame = Frame(self, height = 50)
        self.input_box = Entry(add_player_frame)
        add_player_button = Button(add_player_frame, text="Add Player", command=self.OnAddPlayerButtonPressed)
        self.input_box.pack(side = LEFT)
        add_player_button.pack(side = RIGHT)
        add_player_frame.pack(side = TOP)

    def OnAddPlayerButtonPressed(self):
        player_name = self.input_box.get()
        if len(player_name) > 0:
            self.club.AddPlayer(player_name)
            while self.input_box.get():
                self.input_box.delete(0)
            self.RefreshPlayerList()

    def OnRemovePlayerButtonPressed(self, player):
        self.club.RemovePlayer(player)
        self.RefreshPlayerList()
    
    def HandleInput(self, input):
        return super().HandleInput(input)