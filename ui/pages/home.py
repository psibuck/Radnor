from ui.pages.page_base import PageBase

class HomePage(PageBase):
    
    def __init__(self, manager):
        super().__init__(manager)
        self.name = "home"
        
    def Draw(self):
        print("Type 'cheese' to hear a joke")
    
    def HandleInput(self, input):
        return super().HandleInput(input)
        

