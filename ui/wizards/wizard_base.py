from tkinter import Button, BOTTOM, Frame, Label, LEFT, RIGHT, StringVar, TOP
from ui.pages.page_base import PageBase

class WizardBase(PageBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root)

        self.root_object = object
        self.content_container = Frame(self)
        self.content_container.pack(side=TOP)
        button_container = Frame(self)
        button_container.pack(side=BOTTOM)

        if self.root_object != None:
            Button(button_container, text="Save", command=self.on_edit_pressed).pack(side=LEFT)
            Button(button_container, text="Revert", command=self.on_revert_pressed).pack(side=LEFT)
            Button(button_container, text="Delete", command=self.on_delete_pressed).pack(side=LEFT)

            self.setup_from_object(self.root_object)
        else:
            Button(button_container, text="Add", command=self.on_add_pressed).pack(side=LEFT)

        self.error_message = StringVar()
        Label(self, fg="red", textvariable=self.error_message).pack(side=BOTTOM)

        Button(button_container, text="Cancel", command=self.close).pack(side=RIGHT)

        manager.root.bind('<Return>', self.on_add_pressed)

    def setup_from_object(self, _):
        print("ERROR: setup_from_object not implemented")

    def on_delete_pressed(self):
        success, error = self.handle_delete_pressed()
        if success:
            self.close()
        else:
            self.error_message.set(error)
    
    def on_edit_pressed(self):
        success, error = self.handle_edit_pressed()
        if success:
            self.close()
        else:
            self.error_message.set(error)

    def close(self):
        self.page_manager.on_wizard_closed()
        
    def on_add_pressed(self, _=None):
        success, error = self.handle_add_pressed()
        if success:
            self.close()
        else:
            self.error_message.set(error)

    def on_revert_pressed(self):
        if self.root_object == None:
            print("ERROR: on_revert_pressed has been called but there is no root object")
        else:
            self.setup_from_object(self.root_object)
            
    def handle_add_pressed(self):
        print("ERROR: handle_add_pressed not implemented!")

    def handle_delete_pressed(self):
        print("ERROR: on_delete_pressed not implemented!")
    
    def handle_edit_pressed(self):
        print("ERROR: on_edit_pressed not implemented!")