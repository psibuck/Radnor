from datetime import date
import calendar
from tkinter import Frame, IntVar, Label, OptionMenu, StringVar

MONTHS = [
    ["Jan", 31],
    ["Feb", 28],
    ["Mar", 31],
    ["Apr", 30],
    ["May", 31],
    ["Jun", 30],
    ["Jul", 31],
    ["Aug", 31],
    ["Sep", 30],
    ["Oct", 31],
    ["Nov", 30],
    ["Dec", 31]
]
class DateEntry(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.date_display = None
        
        months = []
        for i in range(len(MONTHS)):
            months.append(i + 1)

        today = date.today()
        self.day = IntVar()
        self.day.set(today.day)
        self.month = IntVar()
        self.month.set(today.month)
        self.month.trace("w", self.UpdateDays)
        self.year = IntVar()
        self.year.set(today.year)
        self.year.trace("w", self.UpdateDays)

        # Year first
        year_buffer = 2
        year = today.year
        years = []
        start_year = year - year_buffer
        end_year = year + year_buffer
        while start_year <= end_year:
            years.append(start_year)
            start_year += 1
        OptionMenu(self, self.year, *years).grid(row=0, column=5)


        # Then month
        OptionMenu(self, self.month, *months).grid(row=0, column=3)

        # combination of two decides how many days 
        self.UpdateDays()

        Label(self, text="D:").grid(row=0, column=0)
        Label(self, text="M:").grid(row=0, column=2)
        Label(self, text="Y:").grid(row=0, column=4)

    def SanitizeDate(self, date):
        str_date = str(date)
        if len(str_date) == 1:
            str_date = "0" + str_date
        return str_date

    def GetDate(self):
        days = self.SanitizeDate(self.day.get())
        months = self.SanitizeDate(self.month.get())
        years = self.SanitizeDate(self.year.get())
        
        return days + months + years

    # Days is set based on the selected year and month
    def UpdateDays(self, *args):
        # if it's February and it's a leap year
        if self.month.get() == 2 and calendar.isleap(self.year.get()):
            self.SetupDateDisplay(29)
        else:
            self.SetupDateDisplay(MONTHS[self.month.get() - 1][1])
    
    def SetupDateDisplay(self, num_days):
        if self.date_display != None:
            self.date_display.grid_forget()

        if self.day.get() > num_days:
            self.day.set(num_days)

        days = []
        i = 1
        while i <= num_days:
            days.append(i)
            i += 1

        self.date_display = OptionMenu(self, self.day, *days)
        self.date_display.grid(row=0, column=1)

            


