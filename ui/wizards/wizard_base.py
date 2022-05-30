from tkinter import Button, BOTTOM, Frame, LEFT, RIGHT, TOP
from ui.pages.page_base import PageBase

class WizardBase(PageBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.content_container = Frame(self)
        self.content_container.pack(side=TOP)
        button_container = Frame(self)
        button_container.pack(side=BOTTOM)
        Button(button_container, text="Add", command=self.handle_add_pressed).pack(side=LEFT)
        Button(button_container, text="Cancel", command=self.close).pack(side=RIGHT)
        
    def close(self):
        self.page_manager.on_wizard_closed()
        
    def handle_add_pressed(self):
        print("ERROR: handle_add_pressed not implemented!")