from tkinter import *
import tkinter as tk
from tkinter import ttk

class ScrollFrame(tk.Frame):

    def __init__(self, root, width=-1):
        tk.Frame.__init__(self, root)

        scroll_canvas = None
        if width != -1:
            scroll_canvas = Canvas(self, width=width)
        else:
            scroll_canvas = Canvas(self)

        scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.content_area = tk.Frame(scroll_canvas)
        self.content_area.pack()

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=scroll_canvas.yview)
        scrollbar.pack(side=RIGHT, fill="y")

        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        self.content_area.bind("<Configure>", func = lambda e: scroll_canvas.configure(scrollregion = scroll_canvas.bbox('all')))
        scroll_canvas.create_window((0,0), window=self.content_area, anchor="nw")

    def clear_children(self):
        for child in self.content_area.winfo_children():
            child.destroy()
        