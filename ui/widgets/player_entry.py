from tkinter import Frame, Label, LEFT

class PlayerEntry(Frame):

    def __init__(self, parent, player):
        Frame.__init__(self, parent)

        self.row = 0
        self.column = 0

        self.player = player
        self.SetupUI()

    def SetupUI(self):
        self.AddControl(Label(self, text = self.player.name))

    def AddControl(self, control_widget):
        control_widget.grid(row=self.row, column=self.column)
        self.column += 1



