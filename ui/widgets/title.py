from tkinter import Label

class Title(Label):

    def __init__(self, parent, text):
        Label.__init__(self, master=parent, text=text, font=('Helvetica bold', 20))