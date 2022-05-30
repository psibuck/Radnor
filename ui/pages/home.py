from select import select
from tkinter import *
from ui.pages.page_base import PageBase
from ui.widgets.table import Table, TableColumn
from ui.wizards.wizard_base import WizardInfo
from ui.wizards.add_player_wizard import AddPlayerWizard

class HomePage(PageBase):
    name = "Club"
    
    def __init__(self, manager, root):
        super().__init__(manager, root)
        
    def SetupContent(self):
        Button(self, text="Add Player", command=self.OnAddPlayerButtonPressed).pack(side=BOTTOM)
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

    def OnAddPlayerButtonPressed(self):
        new_wizard = WizardInfo(AddPlayerWizard)
        self.page_manager.OpenWizard(new_wizard)

    def OnRemovePlayerButtonPressed(self, player):
        self.club.RemovePlayer(player)
        self.RefreshPlayerList()