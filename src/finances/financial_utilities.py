from src.match.fixture import MatchType
from src.match.match_report import MatchReport, MatchRole

def get_match_fee(match: MatchReport, role: MatchRole) -> int:
    """Returns the cost of playing a match, based on the type of match and participant role."""
    if role == MatchRole.UNUSED_SUB:
        return 0
    if match.match_type == MatchType.FRIENDLY:
        return 3

    if match.match_type == MatchType.LEAGUE or match.match_type == MatchType.CUP:
        if role == MatchRole.STARTER:
            return 5
        return 3

def get_amount_string(amount: int) -> str:
    """Returns a visual indication in currency and whether it's positive or negative."""
    prefix = ("+" if amount > 0 else "-") + "£"
    return prefix + str(abs(amount))
