"""The entry_point firebase."""

import json
import os
import firebase_admin
from firebase_admin import db

import src.club.club as Club
import database.json_utilities as JsonUtils

FIREBASE_CONFIG = "config.json"


def save_to_path(path, data):
    ref = db.reference(path)
    ref.set(json.dumps(data))


def save_club(club: Club):
    config = json.load(FIREBASE_CONFIG)

    print(config)

    cred_obj = firebase_admin.credentials.Certificate(
        os.getcwd() + "/firebase/firebase_key.json"
    )
    firebase_admin.initialize_app(cred_obj, config)
    root_path = "/" + club.name

    save_to_path(root_path + "/players/", JsonUtils.convert_to_json(club.players))
    save_to_path(root_path + "/fixtures/", JsonUtils.convert_to_json(club.fixtures))
    save_to_path(
        root_path + "/match_reports/", JsonUtils.convert_to_json(club.match_reports)
    )
    save_to_path(
        root_path + "/training_venues/", JsonUtils.convert_to_json(club.training_venues)
    )
    save_to_path(
        root_path + "/training_reports/",
        JsonUtils.convert_to_json(club.training_reports),
    )
