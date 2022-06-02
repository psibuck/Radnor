from tkinter import Button, Entry, TOP
from ui.wizards.wizard_base import WizardBase

class AddPlayerWizard(WizardBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.input_box = Entry(root)
        self.input_box.pack(side = TOP)

    def handle_add_pressed(self):
        player_name = self.input_box.get()
        if len(player_name) > 0:
            success, error = self.club.add_player(player_name)
            return success, error
        return "No Player Name Entered", False

