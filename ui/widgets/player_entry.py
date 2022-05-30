from tkinter import Frame, Label, LEFT

class PlayerEntry(Frame):

    def __init__(self, parent, player):
        Frame.__init__(self, parent)

        self.row = 0
        self.column = 0

        self.player = player
        self.setup_ui()

    def setup_ui(self):
        self.add_control(Label(self, text = self.player.name))

    def add_control(self, control_widget):
        control_widget.grid(row=self.row, column=self.column)
        self.column += 1



