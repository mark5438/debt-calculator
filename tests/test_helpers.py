from datetime import date, datetime

from dateutil.relativedelta import relativedelta

from debt_calculator.models.debt_item import DebtItem


def calculate_elapsed_month(debt: DebtItem) -> int:
    """
    calculate elapsed month independent from the actual logic code.
    :param debt:
    :return: number of elapsed month
    """
    current_date = date.today()
    start_date = debt.start_date
    return ((current_date.year - start_date.year) * 12) + (current_date.month - start_date.month)


def calculate_remaining_installments(debt: DebtItem, elapsed_number_of_month: int) -> int:
    """
    calculate remaining installments independent from the actual logic code.
    :param elapsed_number_of_month:
    :param debt:
    :return: remaining installments
    """
    return debt.number_of_installments - elapsed_number_of_month


def calculate_remaining_amount(debt: DebtItem, elapsed_number_of_month: int) -> float:
    """
    calculate remaining amount independent from the actual logic code.
    :param debt:
    :param elapsed_number_of_month:
    :return: remaining amount
    """
    payment_so_far = elapsed_number_of_month * debt.installment_amount
    return debt.total_amount - payment_so_far


def calculate_end_date(debt: DebtItem) -> datetime:
    return debt.start_date + relativedelta(months=+debt.number_of_installments)
