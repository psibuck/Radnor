from ui.pages.page_base import PageBase

class PlayerView(PageBase):

    def __init__(self, manager, root, player):
        super().__init__(manager, root)

        self.setup_content()


