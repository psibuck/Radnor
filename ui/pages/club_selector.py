from tkinter import BOTTOM, Button, Label
from ui.pages.page_base import PageBase
from ui.wizards.add_club_wizard import AddClubWizard

class ClubSelector(PageBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root)

    def setup_content(self):
        for club in self.page_manager.app.clubs:
            Button(self, text=club.name, command=lambda c = club: self.select_club(c)).pack()
        
        Button(self, text="Add", command=self.handle_add_club).pack(side=BOTTOM)
    
    def handle_add_club(self):
        self.page_manager.open_subpage(AddClubWizard)
    
    def select_club(self, club):
        self.page_manager.app.select_club(club)