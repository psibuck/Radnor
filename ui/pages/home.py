from tkinter import *
from ui.pages.page_base import PageBase
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
        self.player_list = Table(self, remove_func=self.OnRemovePlayerButtonPressed)
        columns = [TableColumn("Name", "name"), TableColumn("Appearances", function = "GetAppearances"), TableColumn("Training", "training_attendance")]
        self.player_list.AddColumns(columns)
        self.player_list.pack(side=LEFT)
        
        self.RefreshPlayerList()

    def RefreshPlayerList(self):
        self.player_list.ClearRows()

        for player in self.club.players:
            self.player_list.AddObject(player)
        
    def ShowPlayerButtonArea(self):
        add_player_frame = Frame(self, height = 50)
        self.input_box = Entry(add_player_frame)
        self.input_box.grid(row=0, column=0)
        add_player_button = Button(add_player_frame, text="Add Player", command=self.OnAddPlayerButtonPressed)
        add_player_button.grid(row=0,column=1)
        self.error_message = StringVar() 
        Label(add_player_frame, textvariable=self.error_message).grid(row=0, column=2)
        add_player_frame.pack(side = TOP)

    def OnAddPlayerButtonPressed(self):
        player_name = self.input_box.get()
        if len(player_name) > 0:
            success, error = self.club.AddPlayer(player_name)
            if success:
                while self.input_box.get():
                    self.input_box.delete(0)
                self.RefreshPlayerList()
                self.error_message.set("Player Added!")
            else:
                self.error_message.set("ERROR: " + error)


    def OnRemovePlayerButtonPressed(self, player):
        self.club.RemovePlayer(player)
        self.RefreshPlayerList()