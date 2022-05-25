from tkinter import Entry, Frame, Label

class DateEntry(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        entry_width = 2
        Label(self, text="D:").grid(row=0, column=0)

        self.day_entry = Entry(self, width=entry_width)
        self.day_entry.grid(row=0, column=1)

        Label(self, text="M:").grid(row=0, column=2)

        self.month_entry = Entry(self, width=entry_width)
        self.month_entry.grid(row=0, column=3)

        Label(self, text="Y:").grid(row=0, column=4)

        self.year_entry = Entry(self, width=entry_width)
        self.year_entry.grid(row=0, column=5)

    def SanitizeDate(self, widget):
        date = widget.get()
        if len(date) == 1:
            date = "0" + str(date)
        return date

    def GetDate(self):
        days = self.SanitizeDate(self.day_entry)
        months = self.SanitizeDate(self.month_entry)
        years = self.SanitizeDate(self.year_entry)
        
        return days + months + years
