from tkinter import Frame, Label, LEFT

class PlayerEntry(Frame):

    def __init__(self, parent, player):
        Frame.__init__(self, parent)

        self.player = player
        self.SetupUI()

    def SetupUI(self):
        label = Label(self, text = self.player.name)
        label.pack(side = LEFT)


