from tkinter import *
from ui.widgets.object_list import ObjectListWidget

from ui.widgets.player_entry import PlayerEntry

# an ObjectTradingDisplay is a ui display that allows trading of objects between two lists of objects.
class ObjectTradingDisplay(Frame):

    def __init__(self, object_list, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.initial_objects = object_list
        self.selected_objects = []

        label = Label(self, text="test")
        label.pack()

        self.initial_frame = ObjectListWidget(self, "Available Players")
        self.initial_frame.pack(side = LEFT, anchor=N)

        self.selected_frame = ObjectListWidget(self, "First XI")
        self.selected_frame.pack(side = RIGHT, anchor=N)

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
        self.SetupList(self.initial_frame, self.initial_objects, self.SelectObject, "+")
        self.SetupList(self.selected_frame, self.selected_objects, self.DeselectObject, "-")
    
    def SetupList(self, list, objects, action, button_icon):
        list.ClearWidgets()

        widgets = []
        for object in objects:
            entry_widget = PlayerEntry(list, object)
            select_button = Button(entry_widget, text = button_icon, command = lambda w = object: action(w))
            select_button.pack(side = RIGHT)
            widgets.append(entry_widget)
        list.Setup(widgets)