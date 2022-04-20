from tkinter import *
from ui.pages.page_base import PageBase
from ui.widgets.object_list import ObjectListWidget
from ui.widgets.player_entry import PlayerEntry

class HomePage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "Club"

        self.input_box = None
        self.old_player_list = None
        self.player_list = None
        self.frame = None
        
    def SetupContent(self, frame):
        if self.frame == None:
            self.frame = frame

        self.ShowPlayerButtonArea()
        self.ShowPlayerList()
    
    def ShowPlayerList(self):
        if self.player_list == None:
            self.player_list = ObjectListWidget(self.frame, "Player List")
            self.player_list.pack(side=TOP)

        self.player_list.ClearWidgets()

        player_widgets = []
        for player in self.manager.app.club.players:
            entry = PlayerEntry(self.player_list, player)
            remove_button = Button(entry, text = "X", command = lambda: self.OnRemovePlayerButtonPressed(player.name))
            remove_button.pack(side = LEFT)
            player_widgets.append(entry)

        self.player_list.Setup(player_widgets)
        
    def ShowPlayerButtonArea(self):
        add_player_frame = Frame(self.frame, height = 50)
        self.input_box = Entry(add_player_frame)
        add_player_button = Button(add_player_frame, text="Add Player", command=self.OnAddPlayerButtonPressed)
        self.input_box.pack(side = LEFT)
        add_player_button.pack(side = RIGHT)
        add_player_frame.pack()

    def OnAddPlayerButtonPressed(self):
        player_name = self.input_box.get()
        self.manager.app.club.AddPlayer(player_name)
        while self.input_box.get():
            self.input_box.delete(0)
        self.ShowPlayerList()

    def OnRemovePlayerButtonPressed(self, player_name):
        self.manager.app.club.RemovePlayer(player_name)
        self.ShowPlayerList()
    
    def HandleInput(self, input):
        return super().HandleInput(input)

    def Shutdown(self):
        if self.input_box is not None:
            self.input_box.destroy()
        self.frame = None
        if self.old_player_list is not None:
            self.old_player_list.destroy()
            self.old_player_list = None    

        if self.player_list is not None:
            self.player_list.destroy()
            self.player_list = None 

