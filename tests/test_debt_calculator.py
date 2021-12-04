from datetime import datetime

import pytest

from debt_calculator.inner_logic.debt import Debt
from debt_calculator.models.debt_item import DebtItem
from tests.test_helpers import calculate_elapsed_month, calculate_remaining_installments, calculate_remaining_amount, calculate_end_date


@pytest.fixture
def debt_test_item() -> DebtItem:
    """
    Initiate a test object
    :return: DebtItem
    """
    # * Set test values
    debt_item_name = "Car"
    debt_item_total_amount = 1000
    debt_item_number_of_installments = 100
    debt_item_installment_amount = 10
    debt_item_start_date = datetime.strptime("10-10-2021", '%d-%m-%Y')

    return DebtItem(name=debt_item_name,
                    total_amount=debt_item_total_amount,
                    number_of_installments=debt_item_number_of_installments,
                    installment_amount=debt_item_installment_amount,
                    start_date=debt_item_start_date)


def test_valid_installment_input(debt_test_item):
    # * Assert
    assert Debt.is_debt_installment_calculation_valid(debt_test_item)


def test_invalid_installment_input(debt_test_item):
    # * Setup
    debt_test_item.number_of_installments = 1000

    # * Assert
    with pytest.raises(ValueError) as value_error:
        Debt.is_debt_installment_calculation_valid(debt_test_item)


def test_elapsed_month_calculation(debt_test_item):
    # * Setup
    expected_elapsed_month = calculate_elapsed_month(debt_test_item)
    actual_elapsed_month = Debt.calculate_elapsed_month(debt_test_item)

    # * Assert
    assert actual_elapsed_month == expected_elapsed_month


def test_remaining_installments_calculation(debt_test_item):
    # * Setup
    elapsed_month = Debt.calculate_elapsed_month(debt_test_item)
    expected_remaining_installments = calculate_remaining_installments(debt_test_item, elapsed_month)

    # * Assert
    assert Debt.calculate_remaining_installments(debt_test_item, elapsed_month) == expected_remaining_installments


def test_remaining_amount_calculation(debt_test_item):
    # * Setup
    elapsed_month = Debt.calculate_elapsed_month(debt_test_item)
    expected_remaining_amount = calculate_remaining_amount(debt_test_item, elapsed_month)

    # * Assert
    assert Debt.calculate_remaining_amount(debt_test_item, elapsed_month) == expected_remaining_amount


def test_end_date_calculation(debt_test_item):
    # * Setup
    expected_end_date = calculate_end_date(debt_test_item)

    # * Assert
    assert Debt.calculate_end_date(debt_test_item) == expected_end_date
