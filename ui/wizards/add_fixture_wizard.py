from datetime import date
from tkinter import Button, Entry, OptionMenu, StringVar

from src.match.fixture import Fixture, MatchType, Venue
from ui.widgets.date_entry import DateEntry
from ui.widgets.table import TableHeader
from ui.wizards.wizard_base import WizardBase

class AddFixtureWizard(WizardBase):

    def __init__(self, manager, root, object=None):
        super().__init__(manager, root)

        self.date = DateEntry(self.content_container)
        self.date.grid(row=0, column=0, columnspan=5)

        TableHeader(self.content_container, "Match Type").grid(row=1, column=0)
        self.selected_match_type = StringVar()
        self.selected_match_type.set(str(MatchType(1)))
        match_type_selector = OptionMenu(self.content_container, self.selected_match_type, *list(MatchType))
        match_type_selector.grid(row=1, column=1)

        TableHeader(self.content_container, "Venue").grid(row=2, column=0)
        self.selected_venue = StringVar()
        self.selected_venue.set(str(Venue(1)))
        venue_selector = OptionMenu(self.content_container, self.selected_venue, *list(Venue))
        venue_selector.grid(row=2, column=1)

        TableHeader(self.content_container, "Opponent").grid(row=3, column=0)
        self.selected_opponent = StringVar()
        self.opposition_list = None
        if len(self.club.opponents) > 0:
            self.selected_opponent.set(self.club.opponents[0])
            self.add_opposition_list()

        self.oppo_entry = Entry(self.content_container, text="New Opponent")
        self.oppo_entry.grid(row=3, column=2)
        Button(self.content_container, text="+", command=self.add_opponent).grid(row=3, column=3)

    def add_opposition_list(self):
        if self.opposition_list is not None:
            self.opposition_list.grid_forget()
        self.opposition_list = OptionMenu(self.content_container, self.selected_opponent, *list(self.club.opponents))
        self.opposition_list.grid(row=3, column=1)

    def add_opponent(self):
        opponent_name = self.oppo_entry.get()
        if len(opponent_name) > 0:
            self.club.add_opponent(opponent_name)
            self.selected_opponent.set(opponent_name)

            self.add_opposition_list()
            while self.oppo_entry.get():
                self.oppo_entry.delete(0)

    def handle_add_pressed(self):
        new_fixture = Fixture()
        new_fixture.venue = Venue[self.selected_venue.get()]
        new_fixture.match_type = MatchType[self.selected_match_type.get()]
        new_fixture.date = self.date.get_date()
        if new_fixture.date < date.today():
            return False, "Fixture date cannot be in the past"

        new_fixture.opponent = self.selected_opponent.get()
        if new_fixture.opponent == "":
            return False, "No opponent set"

        self.club.add_fixture(new_fixture)
        self.close()

        return True, ""