from tkinter import Button, Frame, Label
from ui.widgets.labels import TableHeader

class TableColumn:

    def __init__(self, name, property_name = None, function = None):
        self.name = name
        self.property = property_name
        self.function = function

class Table(Frame):

    def __init__(self, parent, remove_func=None):
        Frame.__init__(self, parent)
        self.row = 1
        self.columns = list[TableColumn]
        self.remove_func = remove_func

    def AddColumns(self, columns: list[TableColumn]):
        self.columns = columns
        
        col = 0
        for column in self.columns:
            header = TableHeader(self, text=column.name)
            header.grid(row=0, column = col)
            col += 1
        
    def ClearRows(self):
        for widget in self.winfo_children():
            if widget.__class__ is not TableHeader:
                widget.destroy()
        
    def AddObject(self, object):
        col = 0
        for column in self.columns:
            if column.property is not None:
                property_name = column.property
                if not hasattr(object, property_name):
                    print("TABLE ERROR: object does not have expected property")
                else:
                    new_entry = Label(self, text=str(getattr(object, property_name)))
                    new_entry.grid(row = self.row, column = col)
            elif column.function is not None:
                function = column.function
                if not hasattr(object, function):
                    print("TABLE ERROR: object does not have expected function")
                else:
                    new_entry = Label(self, text=str(getattr(object, function)()))
                    new_entry.grid(row = self.row, column = col)
            col += 1
        if self.remove_func is not None:
            remove_button = Button(self, text="X", command= lambda object=object : self.remove_func(object))
            remove_button.grid(row=self.row, column=col)
        self.row += 1