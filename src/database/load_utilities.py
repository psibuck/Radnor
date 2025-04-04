import os
from src.club.club_creation import ClubCreationData
from typing import List

from src.database.settings import DATA_FOLDER


def load_all_clubs() -> List[ClubCreationData]:

    clubs: List[ClubCreationData] = []
    if os.path.exists(DATA_FOLDER):
        for _, dirs, _ in os.walk(DATA_FOLDER):
            for dir_name in dirs:
                clubs.append(ClubCreationData(dir_name, ""))

    return clubs
