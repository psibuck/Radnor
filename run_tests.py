from cgi import test
import os
from os.path import exists
import random
from re import I

from src.club.club import *
from src.club.player import Player
from src.match.match_report import MatchType, MatchReport, Venue

TEST_PLAYERS = ["jack", "steve", "alex", "michael", "peter", "archie", "richard", "thomas", "andrew", "mason", "brad", "phil", "jonny"]
TEST_VENUE_NAMES = ["nou camp", "old trafford", "anfield", "etihad"]
TEST_VENUE_COSTS = [5, 2.50, 6, 10]

def TEST_create_club_and_add_players(test_folder):
    club_one = Club(test_folder)

    for player in TEST_PLAYERS:
        club_one.AddPlayer(player)

    club_one.SaveClub(test_folder)

    club_two = Club(test_folder)
    club_two.Load(test_folder)

    num_players = len(club_one.players)
    if num_players != len(club_two.players):
        print("TEST FAILED: descrepancy in number of players at clubs")
        return False
    else:
        i = 0
        while i < num_players:
            if club_one.players[i].name != club_two.players[i].name:
                print("TEST FAILED: different players loaded than saved")
                return False
            i += 1
    return True

def TEST_create_match_report_and_save_and_load(test_folder):
    club_one = Club(test_folder)
    match_report = MatchReport()

    while len(match_report.starting_lineup) < 11:
        match_report.AddStarter(Player(random.choice(TEST_PLAYERS)))
    while len(match_report.subs) < 5:
        match_report.AddSub(Player(random.choice(TEST_PLAYERS)))

    match_report.match_type = random.choice(list(MatchType))
    match_report.venue = random.choice(list(Venue))

    club_one.AddMatchReport(match_report)
    club_one.SaveClub(test_folder)

    club_two = Club(test_folder)
    club_two.Load(test_folder)

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

    club_one = Club(test_folder)

    while len(club_one.training_venues) < num_venues_to_generate:
        club_one.training_venues.append(TrainingVenue(random.choice(TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS)))

    club_one.SaveClub(test_folder)

    club_two = Club(test_folder)
    club_two.Load(test_folder)

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

    club_one = Club(test_folder)

    while len(club_one.training_venues) < num_reports_to_generate:
        club_one.training_venues.append(TrainingVenue(random.choice(TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS)))

    while len(club_one.training_reports) < num_reports_to_generate:
        new_report = TrainingReport()
        num_attendees = random.randint(0, 20)
        i = 0
        while i < num_attendees:
            new_report.attendees.append(random.choice(TEST_PLAYERS))
            i += 1
        new_report.venue = TrainingVenue(random.choice(TEST_VENUE_NAMES), random.choice(TEST_VENUE_COSTS))
        club_one.training_reports.append(new_report)

    club_one.SaveClub(test_folder)

    club_two = Club(test_folder)
    club_two.Load(test_folder)

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

tests = [TEST_create_club_and_add_players, TEST_create_match_report_and_save_and_load, TEST_create_training_venues_and_save_and_load, TEST_create_training_report_and_save_and_load]

test_folder_name = "test"

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

# TODO - clean-up test files    
    