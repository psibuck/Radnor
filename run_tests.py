import os
import random
import shutil

from src.club.club import *
from src.club.player import Player
from src.training.report import TrainingReport
from src.training.venue import TrainingVenue
from src.match.fixture import MatchType, Venue
from src.match.report import MatchReport
from src.utilities.save_utilities import save_club, load_club

TEST_PLAYERS = [["jack", "charlton"], ["steven", "gerrard"], [
    "alex", "telles"], ["michael", "ballack"], ["peter", "crouch"]]
TEST_VENUE_NAMES = ["nou camp", "old trafford", "anfield", "etihad"]
TEST_VENUE_COSTS = [5, 2.50, 6, 10]


def TEST_create_club_and_add_duplicate_player(test_folder):
    club_one = Club("test_club")

    first_name = "same"
    surname = "name"
    valid, error = club_one.add_player(Player(first_name, surname))

    if valid == False:
        print("TEST FAILED: failed to add player to club. Error: " + error)
        return False

    valid, error = club_one.add_player(Player(first_name, surname))
    if not valid and len(club_one.players) == 1:
        return True

    print("TEST FAILED: successfully added duplicate player to club")
    return False


def TEST_create_club_and_add_players(test_folder):
    club_one = Club("test_club")

    for player in TEST_PLAYERS:
        club_one.add_player(Player(player[0], player[1]))

    save_club(club_one, test_folder)

    club_two = Club("test_club")
    load_club(club_two, test_folder)

    num_players = len(club_one.players)
    if num_players != len(club_two.players):
        print("TEST FAILED: descrepancy in number of players at clubs")
        return False
    else:
        i = 0
        while i < num_players:
            if club_one.players[i] != club_two.players[i]:
                print("TEST FAILED: different players loaded than saved")
                return False
            i += 1
    return True


def TEST_create_match_report_and_save_and_load(test_folder):
    club_one = Club("test_club")
    match_report = MatchReport()

    while len(match_report.starting_lineup) < 11:
        match_report.add_starter(Player(random.choice(TEST_PLAYERS)[
                                 0], random.choice(TEST_PLAYERS)[1]))
    while len(match_report.subs) < 5:
        match_report.add_sub(Player(random.choice(TEST_PLAYERS)[
                             0], random.choice(TEST_PLAYERS)[1]))

    match_report.match_type = random.choice(list(MatchType))
    match_report.venue = random.choice(list(Venue))

    club_one.add_match_report(match_report)
    save_club(club_one, test_folder)

    club_two = Club("test_club")
    load_club(club_two, test_folder)

    if len(club_two.match_reports) != 1:
        return False

    report = club_two.match_reports[0]
    if len(report.starting_lineup) != 11:
        return False
    if len(report.subs) != 5:
        return False
    if match_report.match_type != report.match_type:
        return False
    if match_report.venue != report.venue:
        return False

    return True


def TEST_create_training_venues_and_save_and_load(test_folder):
    num_venues_to_generate = 5

    club_one = Club("test_club")

    while len(club_one.training_venues) < num_venues_to_generate:
        club_one.training_venues.append(TrainingVenue(
            random.choice(TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS)))

    save_club(club_one, test_folder)

    club_two = Club("test_club")
    load_club(club_two, test_folder)

    if len(club_two.training_venues) != num_venues_to_generate:
        print("TEST FAILED: didn't store and load the expected number of venues")
        return False

    if len(club_one.training_venues) != len(club_two.training_venues):
        print("TEST FAILED: failed to load the same amount of training venues back")
        return False

    i = 0
    while i < len(club_two.training_venues):
        club_one_test_venue = club_one.training_venues[i]
        club_two_test_venue = club_two.training_venues[i]

        if club_one_test_venue != club_two_test_venue:
            print("TEST FAILED: discrepancy in data after being saved and loaded")
            return False
        i += 1
    return True


def TEST_create_training_report_and_save_and_load(test_folder):
    num_reports_to_generate = 10

    club_one = Club("test_club")

    while len(club_one.training_venues) < num_reports_to_generate:
        club_one.training_venues.append(TrainingVenue(
            random.choice(TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS)))

    while len(club_one.training_reports) < num_reports_to_generate:
        new_report = TrainingReport()
        num_attendees = random.randint(0, 20)
        i = 0
        while i < num_attendees:
            new_report.attendees.append(random.choice(TEST_PLAYERS))
            i += 1
        new_report.venue = TrainingVenue(random.choice(
            TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS))
        club_one.training_reports.append(new_report)

    save_club(club_one, test_folder)

    club_two = Club("test_club")
    load_club(club_two, test_folder)

    if len(club_two.training_reports) != len(club_one.training_reports):
        print("TEST FAILED: discrepancy in number of training reports after save and load")
        return False

    # TO-DO: functionise this
    i = 0
    while i < len(club_two.training_reports):
        if club_one.training_reports[i] != club_two.training_reports[i]:
            print("TEST FAILED: discrepancy in object data after being saved and loaded")
            return False
        i += 1

    return True


def run_tests():
    count = 0
    successful = 0
    for test_def in tests:
        test_name = test_def.__name__
        print("Running " + test_name + " test")
        if test_def(test_folder_name):
            print(test_name + " passed")
            successful += 1
        else:
            print(test_name + " failed")
        count += 1
    print("we ran " + str(count) + " tests. " + str(successful) + " passes.")

    return count == successful


def clean_up():
    shutil.rmtree(test_folder_name)


test_folder_name = "test/"
os.mkdir("test")
tests = [TEST_create_club_and_add_players,
         TEST_create_club_and_add_duplicate_player,
         TEST_create_match_report_and_save_and_load,
         TEST_create_training_venues_and_save_and_load,
         TEST_create_training_report_and_save_and_load]

if run_tests():
    clean_up()
