import json
from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from debt_calculator.inner_logic.error_messages import ErrorMessages
from debt_calculator.inner_logic.plot import Plot
from debt_calculator.models.debt_item import DebtItem, DebtItems


class Debt:
    # STORE_FILE_PATH = 'book_keeping/debt_store.json'
    STORE_FILE_PATH = '/Users/ahamouda/study_projects/debt-calculator/book_keeping/debt_store.json'

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
            start_date=Debt.get_debt_start_time())

        # Check installment sanity
        Debt.is_debt_installment_calculation_valid(debt_item)

        # Aggregate & calculate the missing debt info
        elapsed_month = Debt.calculate_elapsed_month(debt_item)
        debt_item.remaining_installments = Debt.calculate_remaining_installments(debt_item, elapsed_month)
        debt_item.remaining_amount = Debt.calculate_remaining_amount(debt_item, elapsed_month)
        debt_item.end_date = Debt.calculate_end_date(debt_item)

        # Add item to json file
        Debt.add_item_to_debt_store(debt_item, self.STORE_FILE_PATH)

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
    def add_item_to_debt_store(debt_item, store_file_path) -> None:
        # TODO: update when changing to database
        with open(store_file_path, 'a') as debt_store:
            debt_store.write(f"{debt_item.json()}\n")

    def plot_debt_over_all_period(self):
        # Get items from source
        raw_items_list = self.get_debt_items()
        # Recalculate variable data
        items_list = Debt.calculate_variable_data_for_list(raw_items_list)
        # Get longest debt period
        # TODO: convert this to month instead of numbers
        highest_debt_period = range(1, max(items_list.items, key=lambda x: x.remaining_installments).remaining_installments + 1)
        # Get plot labels
        plot_labels = [item.name for item in items_list.items]
        # Get payments
        # the below will create a list of list with each sublist being the [installment amount * remaining installments]
        monthly_payment_per_item = [[item.installment_amount for i in range(item.remaining_installments)] for item in items_list.items]
        # Send data to be plotted
        # TODO convert all the manual passing of values into an plotItem object
        Plot().plot_a_stackplot(x_axis=highest_debt_period, y_axis=monthly_payment_per_item, labels=plot_labels)

    @staticmethod
    def calculate_variable_data_for_list(items_list: DebtItems) -> DebtItems:
        updated_items = []
        for debt_item in items_list.items:
            elapsed_month = Debt.calculate_elapsed_month(debt_item)
            debt_item.remaining_installments = Debt.calculate_remaining_installments(debt_item, elapsed_month)
            debt_item.remaining_amount = Debt.calculate_remaining_amount(debt_item, elapsed_month)
            debt_item.end_date = Debt.calculate_end_date(debt_item)
            updated_items.append(debt_item)
        return DebtItems(items=updated_items)

    def get_debt_items(self) -> DebtItems:
        return DebtItems(items=self.get_items_from_debt_store(self.STORE_FILE_PATH))

    @staticmethod
    def get_items_from_debt_store(store_file_path) -> list:
        # TODO: update when changing to database
        with open(store_file_path, 'r') as debt_store:
            debt_items = []
            # clean the input
            for item in debt_store.readlines():
                debt_items.append(json.loads(item))
            return debt_items

