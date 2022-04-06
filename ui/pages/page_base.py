

class PageBase:

    def __init__(self, manager):
        self.manager = manager

    def HandleInput(self, input):
        self.manager.HandleInput(input)

    def Draw(self):
        return