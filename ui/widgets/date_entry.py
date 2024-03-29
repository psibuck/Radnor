from datetime import date
import calendar
from tkinter import Frame, IntVar, Label, OptionMenu

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

    def __init__(self, parent, vertical = False, default_date: date = date.today(), years_to_show = 1, end_year = -1, start_year = -1):
        Frame.__init__(self, parent)
        self.date_display = None
        self.vertical = vertical
        
        months = []
        for i in range(len(MONTHS)):
            months.append(i + 1)

        self.day = IntVar()
        self.day.set(default_date.day)
        self.month = IntVar()
        self.month.set(default_date.month)
        self.month.trace("w", self.update_days)
        self.year = IntVar()
        self.year.set(default_date.year)
        self.year.trace("w", self.update_days)

        self.row = 0
        self.column = 0
        
        # Year first
        if end_year == -1:
            year = default_date.year
        else:
            year = end_year

        years = []
        if start_year == -1:
            start_year = year - int(0.5 * years_to_show)

        if end_year == -1:
            end_year = year + int(0.5 * years_to_show)

        while start_year <= end_year:
            years.append(start_year)
            start_year += 1
        year_menu = OptionMenu(self, self.year, *years)
        # Then month
        month_menu = OptionMenu(self, self.month, *months)
        # combination of two decides how many days 
        self.update_days()

        self.add_to_grid(Label(self, text="D:"), self.date_display)
        self.add_to_grid(Label(self, text="M:"), month_menu)
        self.add_to_grid(Label(self, text="Y:"), year_menu)

    def sanitize_data(self, date):
        str_date = str(date)
        if len(str_date) == 1:
            str_date = "0" + str_date
        return str_date

    def set_date(self, date: date):
        self.day.set(date.day)
        self.month.set(date.month)
        self.year.set(date.year)

    def get_date(self):
        days = self.sanitize_data(self.day.get())
        months = self.sanitize_data(self.month.get())
        years = self.sanitize_data(self.year.get())
        return date.fromisoformat(years + "-" + months + "-" + days)

    def add_to_grid(self, label, widget):
        label.grid(column = self.column, row = self.row)
        widget.grid(column = self.column + 1, row = self.row)

        if self.vertical:
            self.row += 1
        else:
            self.column += 2

    # Days is set based on the selected year and month
    def update_days(self, *args):
        # if it's February and it's a leap year
        if self.month.get() == 2 and calendar.isleap(self.year.get()):
            self.setup_date_display(29)
        else:
            self.setup_date_display(MONTHS[self.month.get() - 1][1])
        self.date_display.grid(row=0, column=1)
    
    def setup_date_display(self, num_days):
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
            


