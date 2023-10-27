from dataclasses import dataclass


@dataclass
class ClubCreationData:
    """Data class that contains all the information needed to create a club."""
    name: str
    short_name: str

    def __lt__(self, other_club: 'ClubCreationData') -> bool:
        return self.short_name < other_club.short_name

    def __gt__(self, other_club: 'ClubCreationData') -> bool:
        return self.short_name > other_club.short_name
