from email import header
from tkinter import Button, Frame, Label
from tkinter.messagebox import askyesno
from ui.widgets.labels import TableHeader

class TableColumn:

    def __init__(self, name, property_name = None, function = None):
        self.name = name
        self.property = property_name
        self.function = function

class Table(Frame):

    def __init__(self, parent, remove_func=None, header_text=""):
        Frame.__init__(self, parent)
        self.row = 0
        self.columns = []
        self.remove_func = remove_func
        self.header_text = header_text
        self.header = None

        self.add_header()
    
    def add_header(self):
        if self.header is not None:
            self.header.grid_forget()
        elif self.header_text != "":
            self.row += 1

        if self.header_text != "":
            span = 1
            if len(self.columns) > 0:
                span = len(self.columns)
            self.header = TableHeader(self, text=self.header_text)
            self.header.grid(row=0, column=0, columnspan=span)

    def add_columns(self, columns: list[TableColumn]):
        self.columns = columns
        
        col = 0
        for column in self.columns:
            header = TableHeader(self, text=column.name)
            header.grid(row=self.row, column = col)
            col += 1
        
        self.row += 1
        self.add_header()
        
    def clear_rows(self):
        for widget in self.winfo_children():
            if widget.__class__ is not TableHeader:
                widget.destroy()
        
    def add_object(self, object):
        col = 0
        for column in self.columns:
            if column.property is not None:
                property_name = column.property
                if not hasattr(object, property_name):
                    print("TABLE ERROR: object does not have expected property: " + str(property_name))
                else:
                    new_entry = Label(self, text=str(getattr(object, property_name)))
                    new_entry.grid(row = self.row, column = col)
            elif column.function is not None:
                function = column.function
                if not hasattr(object, function):
                    print("TABLE ERROR: object does not have expected function: " + str(function))
                else:
                    new_entry = Label(self, text=str(getattr(object, function)()))
                    new_entry.grid(row = self.row, column = col)
            col += 1
        if self.remove_func is not None:
            remove_button = Button(self, text="X", command= lambda object=object : self.show_confirmation_dialog(object))
            remove_button.grid(row=self.row, column=col)
        self.row += 1

    def show_confirmation_dialog(self, object):
        message = "Are you sure you want to permanently delete {object_name}".format(object_name=object)
        answer = askyesno("Delete Object", message)
        if answer:
            self.remove_func(object)