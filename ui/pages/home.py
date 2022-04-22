from tkinter import *
from ui.pages.page_base import PageBase
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.player_entry import PlayerEntry

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

        player_widgets = []
        for player in self.club.players:
            entry = PlayerEntry(self.player_list, player)
            remove_button = Button(entry, text = "X", command = lambda: self.OnRemovePlayerButtonPressed(player.name))
            remove_button.pack(side = LEFT)
            player_widgets.append(entry)

        self.player_list.Setup(player_widgets)
        
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

    def OnRemovePlayerButtonPressed(self, player_name):
        self.club.RemovePlayer(player_name)
        self.RefreshPlayerList()
    
    def HandleInput(self, input):
        return super().HandleInput(input)