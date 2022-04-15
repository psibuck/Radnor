from tkinter import *

from ui.widgets.player_entry import PlayerEntry

# an ObjectTradingDisplay is a ui display that allows trading of objects between two lists of objects.
class ObjectTradingDisplay:

    def __init__(self, object_list, parent):
        self.initial_objects = object_list
        self.selected_objects = []
        self.frame = Frame(parent)
        self.frame.pack()

        label = Label(self.frame, text="test")
        label.pack()

        self.initial_frame = Frame(self.frame)
        self.initial_frame.pack(side = LEFT)

        self.selected_frame = Frame(self.frame)
        self.selected_frame.pack(side = RIGHT)

        self.SetupObjectLists()

    def SelectObject(self, object):
        self.SwapObject(self.initial_objects, self.selected_objects, object)
    
    def DeselectObject(self, object):
        self.SwapObject(self.selected_objects, self.initial_objects, object)
    
    def SwapObject(self, current_list, new_list, object):
        if object in current_list:
            current_list.remove(object)
            new_list.append(object)
            new_list.sort()

            self.SetupObjectLists()

    def SetupObjectLists(self):
        for widget in self.initial_frame.winfo_children():
            widget.destroy()
        for widget in self.selected_frame.winfo_children():
            widget.destroy()

        for entry in self.initial_objects:
            entry_widget = PlayerEntry(self.initial_frame, entry)
            select_button = Button(entry_widget.frame, text = "+", command = lambda object = entry: self.SelectObject(object))
            select_button.pack(side = RIGHT)
        
        for entry in self.selected_objects:
            entry_widget = PlayerEntry(self.selected_frame, entry)
            remove_button = Button(entry_widget.frame, text = "X", command = lambda object = entry: self.DeselectObject(object))
            remove_button.pack(side = RIGHT)