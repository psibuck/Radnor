from src.utilities.data_utilities import json_get

class Goal:

    def __init__(self, scorer="None", assister="None", description=""):
        self.scorer = scorer
        self.assister = assister
        self.description = description

    def from_json(self, json_data):
        self.scorer = json_get(json_data, "scorer")
        self.assister = json_get(json_data, "assister")
        self.description = json_get(json_data, "description")

    def to_json(self):
        return {
            "scorer": self.scorer,
            "assister": self.assister,
            "description": self.description
        }