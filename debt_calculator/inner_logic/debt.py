from datetime import datetime

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

        # Add item to csv file
        Debt.add_item_to_debt_store(debt_item, self.store_file_path)

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
