from tkinter import Button, BOTTOM
from ui.pages.page_base import PageBase

class WizardInfo:

    def __init__(self, wizard_class):
        self.wizard_class = wizard_class 

class WizardBase(PageBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        Button(root, text="Add", command=self.handle_add_pressed).pack(side=BOTTOM)
        
    def Close(self):
        self.page_manager.OnWizardClosed()
        
    def handle_add_pressed(self):
        print("ERROR: handle_add_pressed not implemented!")