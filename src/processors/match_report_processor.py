from src.club.club import Club
from src.match.report import MatchReport


class MatchReportProcessor:

    @staticmethod
    def add_match_report(club: Club, report: MatchReport):
        club.match_reports.append(report)
        MatchReportProcessor.process_match_report(club, report)
        club.match_reports.sort()
        if club.update_callback != None:
            club.update_callback()

    @staticmethod
    def process_match_reports(club: Club):
        for report in club.match_reports:
            MatchReportProcessor.process_match_report(club, report)

    @staticmethod
    def process_match_report(club: Club, report: MatchReport, add=True):
        increment = 1
        if not add:
            increment = -1

        for starter in report.starting_lineup:
            player = club.get_player_by_name(starter)
            if player is not None:
                player.matches_started += increment

        for sub in report.subs:
            player = club.get_player_by_name(sub)
            if player is not None:
                player.matches_as_sub += increment

        for goal in report.goals:
            scorer = club.get_player_by_name(goal.scorer)
            if scorer is not None:
                scorer.goals += increment
            assister = club.get_player_by_name(goal.assister)
            if assister is not None:
                assister.assists += increment

    @staticmethod
    def remove_match_report(club: Club, report: MatchReport):
        club.match_reports.remove(report)
        MatchReportProcessor.process_match_report(club, report, False)
