from datetime import datetime

from pydantic import BaseModel


class DebtItem(BaseModel):
    name: str
    total_amount: float
    number_of_installments: int
    installment_amount: float
    start_date: datetime
    end_date: datetime = None
    remaining_installments: int = None
    remaining_amount: float = None


class DebtItems(BaseModel):
    items: list[DebtItem]