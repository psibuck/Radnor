from tkinter import Button, BOTTOM
from ui.pages.page_base import PageBase

class WizardBase(PageBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        Button(root, text="Add", command=self.handle_add_pressed).pack(side=BOTTOM)
        
    def close(self):
        self.page_manager.on_wizard_closed()
        
    def handle_add_pressed(self):
        print("ERROR: handle_add_pressed not implemented!")