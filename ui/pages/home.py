from tkinter import *
from ui.pages.page_base import PageBase
from ui.widgets.player_entry import PlayerEntry

class HomePage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "Club"

        self.input_box = None
        self.player_list = None
        self.frame = None
        
    def SetupContent(self, frame):
        self.frame = frame

        self.ShowPlayerButtonArea()
        self.ShowPlayerList()

    
    def ShowPlayerList(self):
        if self.player_list == None:
            self.player_list = Frame(self.frame)
            self.player_list.pack(fill=BOTH, expand=YES)
        else:
            for widget in self.player_list.winfo_children():
                widget.destroy()

        for player in self.manager.app.club.players:
            PlayerEntry(self.player_list, player.name, self.OnRemovePlayerButtonPressed)
        
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
        

