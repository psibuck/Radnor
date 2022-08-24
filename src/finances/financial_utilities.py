from src.match.fixture import MatchType
from src.match.match_report import MatchReport, MatchRole

def get_match_fee(match: MatchReport, role: MatchRole) -> int:
    if role == MatchRole.UNUSED_SUB:
        return 0
    if match.match_type == MatchType.FRIENDLY:
        return 3
    
    if match.match_type == MatchType.LEAGUE or match.match_type == MatchType.CUP:
        if role == MatchRole.STARTER:
            return 5
        return 3

def get_amount_string(amount: int) -> str:
    prefix = ("+" if amount > 0 else "-") + "£"
    return prefix + str(abs(amount))