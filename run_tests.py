from cgi import test
import os
from os.path import exists

from src.club.club import *
from src.club.player import Player

def TEST_create_club_and_add_players(test_file):
    print("Running create club and add players test")

    club_one = Club()

    test_players = ["jack", "steve", "alex"]
    for player in test_players:
        club_one.AddPlayer(player)

    club_one.SaveClub(test_file)

    club_two = Club()
    club_two.LoadPlayers(test_file)

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

tests = [TEST_create_club_and_add_players]

test_file_name = "test_player_list.txt"

count = 0
successful = 0
for test_def in tests:
    if test_def(test_file_name):
        print(str(test_def.__name__) + " passed")
        successful += 1
    else:
        print(str(test_def.__name__) + " failed")
    count += 1
    os.remove(test_file_name)

print("we ran " + str(count) + " tests. " + str(successful) + " passes.")
    
    