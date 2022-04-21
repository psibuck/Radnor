from cgi import test
import os
from os.path import exists
import random

from src.club.club import *
from src.club.player import Player
from src.match.match_report import MatchReport

def TEST_create_club_and_add_players(test_folder):
    print("Running create club and add players test")

    club_one = Club(test_folder)

    test_players = ["jack", "steve", "alex"]
    for player in test_players:
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
    print("Running create match report and save and load test")

    club_one = Club(test_folder)
    match_report = MatchReport()
    test_players = ["jack", "steve", "alex", "michael", "peter", "archie", "richard", "thomas", "andrew", "mason", "brad", "phil", "jonny"]

    while len(match_report.starting_lineup) < 11:
        match_report.AddStarter(Player(random.choice(test_players)))
    while len(match_report.subs) < 5:
        match_report.AddSub(Player(random.choice(test_players)))

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
    
    return True   

tests = [TEST_create_club_and_add_players, TEST_create_match_report_and_save_and_load]

test_folder_name = "test"

count = 0
successful = 0
for test_def in tests:
    if test_def(test_folder_name):
        print(str(test_def.__name__) + " passed")
        successful += 1
    else:
        print(str(test_def.__name__) + " failed")
    count += 1

print("we ran " + str(count) + " tests. " + str(successful) + " passes.")

# TODO - clean-up test files    
    