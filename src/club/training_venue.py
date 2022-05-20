
# A training venue is a location that hosts training. It has an associated cost 
class TrainingVenue:
    
    def __init__(self, name = "", cost = 0.0):
        self.name = name
        self.cost = cost

    def __eq__(self, other):
        return self.name == other.name and self.cost == other.cost

    def __str__(self):
        return self.name
        
    def Save(self, file):
        file.write(self.Stringify() + "\n")

    def Load(self, file):
        data = file.split(",")
        if len(data) != 2:
            print("Error: failed to load training venue, incorrect data")
            return
        self.name = data[0]
        self.cost = float(data[1])

    def Stringify(self):
        return str(str(self.name) + "," + str(self.cost))

    def ToJson(self):
        return {
            "name": self.name,
            "cost": self.cost
        }
    
    def FromJson(self, json_data):
        self.name = json_data["name"]
        self.cost = json_data["cost"]



