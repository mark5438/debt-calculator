from dataclasses import dataclass
from datetime import datetime


@dataclass
class DebtItem:
    name: str
    total_amount: float
    number_of_installments: int
    installment_amount: float
    start_date: datetime
