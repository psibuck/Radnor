from tkinter import Button, Frame, Label, LEFT, RIGHT

class PlayerEntry:

    def __init__(self, owner, player_name, remove_command):
        self.name = player_name
        self.parent = owner
        self.SetupUI(remove_command)

    def SetupUI(self, remove_command):
        frame = Frame(self.parent)
        frame.pack()

        label = Label(frame, text = self.name)
        label.pack(side = LEFT)

        remove_button = Button(frame, text = "X", command = lambda name = self.name: remove_command(name))
        remove_button.pack(side = RIGHT)



