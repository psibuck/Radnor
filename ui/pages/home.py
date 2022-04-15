from tkinter import *
from ui.pages.page_base import PageBase

class HomePage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "Club"

        self.input_box = None
        self.player_list = None
        self.frame = None
        
    def SetupContent(self, frame):
        if self.frame == None:
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
            new_label = Label(self.player_list, text = player.name)
            new_label.pack(side = TOP)
        
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
    
    def HandleInput(self, input):
        return super().HandleInput(input)

    def Shutdown(self):
        if self.input_box is not None:
            self.input_box.destroy()
        self.frame = None
        if self.player_list is not None:
            self.player_list.destroy()
            self.player_list = None     

