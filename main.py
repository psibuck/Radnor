import sys
from src.application import Application
from ui.page_manager import PageManager
from fastapi import FastAPI

app = "app" in sys.argv

if app:
    is_debug = "debug" in sys.argv

    # Refactor this, consider role of page manager vs app, same thing?
    app = Application(is_debug)
    ui = PageManager(app)
    ui.draw()

else:
    app = FastAPI()
    application = Application(True)
    application.select_club(application.clubs[0])

    @app.get("/")
    def home():
        return {"message": "Hello Radnor!"}

    @app.get("/player_list")
    def greet():
        club_names = [club.name for club in application.clubs]
        return {"message": f"{club_names}!"}
