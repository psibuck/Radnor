"""Contains the transaction class and associated helpers"""
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    """Transaction type designates the type of transaction being passed."""
    MATCH = 1
    TRAINING = 2
    PAYMENT = 3
    SIGN_ON = 4
    FINE = 5

    def __str__(self):
        return self.name

class Transaction:
    """A transaction is a class that represents a financial transaction between the club and a third party."""
    def __init__(self, party: str, date: datetime, type_in: TransactionType, amount: int, notes = ""):
        self.party = party
        self.date: datetime = date
        self.transaction_type: TransactionType = type_in
        self.amount: int = amount
        self.notes: str = notes

    def __str__(self):
        return self.date.isoformat() + ": " + self.transaction_type.__str__().upper() + " " + self._get_amount_string() + " " + self.notes

    def _get_amount_string(self) -> str:
        prefix = "+" if self.transaction_type == TransactionType.PAYMENT else "-"
        return prefix + "£" + str(self.amount)
    
    def get_amount(self) -> int:
        """Returns the amount of the transaction, positive for a deposit, negative for a cost."""
        if self.transaction_type == TransactionType.PAYMENT:
            return self.amount
        return -self.amount