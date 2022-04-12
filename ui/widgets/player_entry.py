from tkinter import Button, Frame, Label, LEFT, RIGHT

class PlayerEntry:

    def __init__(self, owner, player_name):
        self.name = player_name
        self.frame = None
        self.parent = owner
        self.SetupUI()

    def SetupUI(self):
        self.frame = Frame(self.parent)
        self.frame.pack()

        label = Label(self.frame, text = self.name)
        label.pack(side = LEFT)



