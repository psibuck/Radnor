from tkinter import Button, BOTTOM, Frame, Label, LEFT, RIGHT, StringVar, TOP
from ui.pages.page_base import PageBase

class WizardBase(PageBase):

    def __init__(self, manager, root):
        super().__init__(manager, root)

        self.content_container = Frame(self)
        self.content_container.pack(side=TOP)
        button_container = Frame(self)
        button_container.pack(side=BOTTOM)
        Button(button_container, text="Add", command=self.on_add_pressed).pack(side=LEFT)

        self.error_message = StringVar()
        Label(button_container, textvariable=self.error_message).pack(side=RIGHT)

        Button(button_container, text="Cancel", command=self.close).pack(side=RIGHT)

        manager.root.bind('<Return>', self.on_add_pressed)

    def close(self):
        self.page_manager.on_wizard_closed()
        
    def on_add_pressed(self, _=None):
        success, error = self.handle_add_pressed()
        if success:
            self.close()
        else:
            self.error_message.set(error)
            
    def handle_add_pressed(self):
        print("ERROR: handle_add_pressed not implemented!")