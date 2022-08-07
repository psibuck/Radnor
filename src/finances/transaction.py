from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TransactionType(Enum):
    MATCH = 1
    TRAINING = 2
    PAYMENT = 3 
    SIGN_ON = 4

    def __str__(self):
        return self.name

@dataclass
class Transaction:

    def __init__(self, date: datetime, type: TransactionType, amount: int, notes = ""):
        self.date: datetime = date
        self.transaction_type: TransactionType = type 
        self.amount: int = amount 
        self.notes: str = notes

    def __str__(self):
        return self.date.isoformat() + ": " + self.transaction_type.__str__().upper() + " " + self._get_amount_string() + " " + self.notes

    def _get_amount_string(self) -> str:
        prefix = "+" if self.transaction_type == TransactionType.PAYMENT else "-"
        return prefix + "£" + str(self.amount)
    
    def get_amount(self) -> int:
        if self.transaction_type == TransactionType.PAYMENT:
            return self.amount
        return -self.amount