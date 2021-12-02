from enum import Enum


class ErrorMessages(Enum):
    INVALID_INSTALLMENT = "Installment amount over the provided total number of installments doesn't equal the total amount!"
