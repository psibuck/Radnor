from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno

from ui.widgets.labels import TableHeader

class TableColumn:

    def __init__(self, name, property_name=None, function=None):
        self.name = name
        self.property = property_name
        self.function = function

class Table(Frame):

    def __init__(self, parent, remove_func=None, select_func=None, header_text="", show_scroll=False):
        Frame.__init__(self, parent)
        self.row = 0
        self.columns = []
        self.remove_func = remove_func
        self.select_func = select_func
        self.header_text = header_text
        self.header = None


        table_canvas = Canvas(self)
        table_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.frame = Frame(table_canvas)
        table_canvas.create_window((0,0), window=self.frame, anchor="nw")

        if show_scroll:
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=table_canvas.yview)
            scrollbar.pack(side=RIGHT, fill="y")

            table_canvas.configure(yscrollcommand=scrollbar.set)
            table_canvas.bind("<Configure>", func = lambda e: table_canvas.configure(scrollregion = table_canvas.bbox('all')))


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
            self.header = TableHeader(self.frame, text=self.header_text)
            self.header.grid(row=0, column=0, columnspan=span)

    def add_columns(self, columns: list[TableColumn]):
        self.columns = columns
        
        col = 0
        for column in self.columns:
            header = TableHeader(self.frame, text=column.name)
            header.grid(row=self.row, column = col)
            col += 1
        
        self.row += 1
        self.add_header()
        
    def clear_rows(self):
        for widget in self.frame.winfo_children():
            if widget.__class__ is not TableHeader:
                widget.destroy()
        
    def add_object(self, object):
        col = 0
        
        if self.select_func != None:
            select_button = Button(self.frame, text="",command=lambda object=object : self.handle_row_select(object))
            select_button.grid(row=self.row, columnspan=len(self.columns), sticky="news")

        for column in self.columns:
            if column.property is not None:
                property_name = column.property
                if not hasattr(object, property_name):
                    print("TABLE ERROR: object does not have expected property: " + str(property_name))
                else:
                    new_entry = Label(self.frame, text=str(getattr(object, property_name)))
                    new_entry.grid(row = self.row, column = col)
            elif column.function is not None:
                function = column.function
                if not hasattr(object, function):
                    print("TABLE ERROR: object does not have expected function: " + str(function))
                else:
                    new_entry = Label(self.frame, text=str(getattr(object, function)()))
                    new_entry.grid(row = self.row, column = col)
            col += 1
        if self.remove_func is not None:
            remove_button = Button(self.frame, text="X", command=lambda object=object : self.show_confirmation_dialog(object))
            remove_button.grid(row=self.row, column=col)
        self.row += 1

    def show_confirmation_dialog(self, object):
        message = "Are you sure you want to permanently delete {object_name}".format(object_name=object)
        answer = askyesno("Delete Object", message)
        if answer:
            self.remove_func(object)

    def handle_row_select(self, object):
        if self.select_func != None:
            self.select_func(object)
        else:
            print("ERROR: row selected but no select function provided")