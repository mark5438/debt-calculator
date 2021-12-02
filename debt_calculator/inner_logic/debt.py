from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from debt_calculator.inner_logic.error_messages import ErrorMessages
from debt_calculator.models.debt_item import DebtItem


class Debt:
    def __init__(self):
        self.store_file_path = 'book_keeping/debt_store.json'

    @staticmethod
    def get_debt_start_time():
        date_format = '%d-%m-%Y'
        prompt_message = "Enter debt start day in the dd-mm-yyyy format \n"
        raw_date = input(prompt_message)
        return datetime.strptime(raw_date, date_format)

    def add_a_debt(self):
        # Collect debt data
        debt_item = DebtItem(
            name=input("Enter Item name: \n"),
            total_amount=float(input("Enter total amount: \n")),
            number_of_installments=int(input("Enter number of installments: \n")),
            installment_amount=float(input("Enter installment amount: \n")),
            start_date=Debt.get_debt_start_time()
        )

        # Check installment sanity
        Debt.is_debt_installment_calculation_valid(debt_item)

        # Aggregate & calculate the missing debt info
        elapsed_month = Debt.calculate_elapsed_month(debt_item)
        debt_item.remaining_installments = Debt.calculate_remaining_installments(debt_item, elapsed_month)
        debt_item.remaining_amount = Debt.calculate_remaining_amount(debt_item, elapsed_month)
        debt_item.end_date = Debt.calculate_end_date(debt_item)

        # Add item to json file
        Debt.add_item_to_debt_store(debt_item, self.store_file_path)

    @staticmethod
    def calculate_elapsed_month(debt: DebtItem) -> int:
        current_date = date.today()
        start_date = debt.start_date
        return ((current_date.year - start_date.year) * 12) + (current_date.month - start_date.month)

    @staticmethod
    def calculate_remaining_installments(debt: DebtItem, elapsed_number_of_month: int) -> int:
        return debt.number_of_installments - elapsed_number_of_month

    @staticmethod
    def calculate_remaining_amount(debt: DebtItem, elapsed_number_of_month: int) -> float:
        payment_so_far = elapsed_number_of_month * debt.installment_amount
        return debt.total_amount - payment_so_far

    @staticmethod
    def calculate_end_date(debt: DebtItem) -> datetime:
        return debt.start_date + relativedelta(months=+debt.number_of_installments)

    @staticmethod
    def is_debt_installment_calculation_valid(item):
        if (item.installment_amount * item.number_of_installments) == item.total_amount:
            return True
        else:
            raise ValueError(ErrorMessages.INVALID_INSTALLMENT.value)

    @staticmethod
    def add_item_to_debt_store(debt_item, store_file_path):
        with open(store_file_path, 'a') as debt_store:
            debt_store.write(f"{debt_item.json()}\n")
