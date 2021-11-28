from datetime import datetime

from debt_calculator.models.debt_item import DebtItem


class Debt:
    def __init__(self):
        pass

    @staticmethod
    def get_debt_start_time():
        date_format = '%d-%m-%Y'
        prompt_message = "Enter debt start day in the dd-mm-yyyy format \n"
        raw_date = input(prompt_message)
        return datetime.strptime(raw_date, date_format)

    def add_a_debt(self):
        debt_item = DebtItem(
            name=input("Enter Item name: \n"),
            total_amount=float(input("Enter total amount: \n")),
            number_of_installments=int(input("Enter number of installments: \n")),
            installment_amount=float(input("Enter installment amount: \n")),
            start_date=Debt.get_debt_start_time()
        )
