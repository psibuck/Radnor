"""The transaction manager is concerned with creating, deleting and modifying transactions."""
from typing import Union

import src.club.player as Player
from src.finances.transaction import Transaction


def load_transactions_from_csv() -> list[str]:
    """Loads the transactions from csv into memory as a list of raw csv strings."""
    return []

def get_transaction_from_raw(raw_transaction: str) -> Union[Transaction, None]:
    """Takes a raw string csv of a transaction and attempts to build a transaction object."""
    return None

def get_player_transactions(player: Player.Player) -> list[Transaction]:
    """Returns a list of the players transactions."""
    transactions_out: list[Transaction] = []
    raw_transactions = load_transactions_from_csv()
    for transaction in raw_transactions:
        processed_transaction: Union[Transaction, None] = get_transaction_from_raw(transaction)
        if processed_transaction is not None:
            if processed_transaction.party in player.aliases:
                transactions_out.append(processed_transaction)
    return transactions_out
