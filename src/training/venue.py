
# A training venue is a location that hosts training. It has an associated cost
class TrainingVenue:

    def __init__(self, name="", cost: float = 0.0):
        self.name = name
        self.cost: float = cost

    def __eq__(self, other):
        if other is None:
            return False
        return self.name == other.name and self.cost == other.cost

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "cost": self.cost
        }

    def from_json(self, json_data):
        self.name = json_data["name"]
        self.cost = float(json_data["cost"])
