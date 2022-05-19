from tkinter import Frame, Label

class TableColumn:

    def __init__(self, name, property):
        self.name = name
        self.property = property

class Table(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.row = 1
        self.columns = list[TableColumn]

    def AddColumns(self, columns: list[TableColumn]):
        self.columns = columns
        
        col = 0
        for column in self.columns:
            header = Label(self, text=column.name)
            header.grid(row=0, column = col)
            col += 1
        
    def AddObject(self, object):
        col = 0
        for column in self.columns:
            property_name = column.property
            if not hasattr(object, property_name):
                print("TABLE ERROR: object does not have expected property")
            else:
                new_entry = Label(self, text=str(getattr(object, property_name)))
                new_entry.grid(row = self.row, column = col)
                col += 1
        self.row += 1