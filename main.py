import sys
from src.application import Application
from ui.page_manager import PageManager
from fastapi import FastAPI

is_app = "app" in sys.argv
is_debug = "debug" in sys.argv

radnor_app = Application(is_debug)

if is_app:
    # Refactor this, consider role of page manager vs app, same thing?
    ui = PageManager(radnor_app)
    ui.draw()

else:
    app = FastAPI()
    radnor_app.select_club(radnor_app.clubs[0])

    @app.get("/")
    def home():
        return {"message": "Hello Radnor!"}

    @app.get("/player_list")
    def greet():
        club_names = [club.name for club in radnor_app.clubs]
        return {"message": f"{club_names}!"}
