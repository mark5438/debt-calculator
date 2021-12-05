import json

# STORE_FILE_PATH = 'book_keeping/debt_store.json'
STORE_FILE_PATH = '/Users/ahamouda/study_projects/debt-calculator/book_keeping/debt_store.json'


class DataStore:

    @staticmethod
    def add_item_to_debt_store(debt_item, store_file_path=STORE_FILE_PATH) -> None:
        # TODO: update when changing to database
        with open(store_file_path, 'a') as debt_store:
            debt_store.write(f"{debt_item.json()}\n")

    @staticmethod
    def get_items_from_debt_store(store_file_path = STORE_FILE_PATH) -> list:
        # TODO: update when changing to database
        with open(store_file_path, 'r') as debt_store:
            debt_items = []
            # clean the input
            for item in debt_store.readlines():
                debt_items.append(json.loads(item))
            return debt_items
