
import sys
from src.application import Application
from ui.page_manager import PageManager

is_debug = "debug" in sys.argv

# Refactor this, consider role of page manager vs app, same thing?
app = Application(is_debug)
ui = PageManager(app)
ui.draw()
