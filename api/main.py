from fastapi import FastAPI
from src.application import Application

app = FastAPI()
application = Application(True)
application.select_club(application.clubs[0])


@app.get("/")
def home():
    return {"message": "Hello, Radnor App!"}


@app.get("/player_list")
def greet():
    club_names = [club.name for club in application.clubs]
    return {"message": f"{club_names}!"}
