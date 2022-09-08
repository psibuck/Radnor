import src.utilities.json_utilities as JsonUtil

class Goal:

    def __init__(self, scorer="None", assister="None", description=""):
        self.scorer = scorer
        self.assister = assister
        self.description = description

    def from_json(self, json_data):
        self.scorer = JsonUtil.get(json_data, "scorer")
        self.assister = JsonUtil.get(json_data, "assister")
        self.description = JsonUtil.get(json_data, "description")

    def to_json(self):
        return {
            "scorer": self.scorer,
            "assister": self.assister,
            "description": self.description
        }