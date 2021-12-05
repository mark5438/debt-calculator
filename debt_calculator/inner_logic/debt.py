from datetime import datetime, date

from dateutil.relativedelta import relativedelta

from debt_calculator.inner_logic.error_messages import ErrorMessages
from debt_calculator.models.debt_item import DebtItem, DebtItems
from debt_calculator.service.data_store import DataStore
from debt_calculator.service.plot import Plot


class Debt:

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
        DataStore.add_item_to_debt_store(debt_item)

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
        return DebtItems(items=DataStore.get_items_from_debt_store())
