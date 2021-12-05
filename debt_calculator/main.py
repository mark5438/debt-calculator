from debt_calculator.inner_logic.debt import Debt


def main():
    # mode = 'a'
    debt = Debt()
    # mode = input("Enter (a) for adding a new item \nEnter (p) for plotting current items\n")
    while input("Enter (a) for adding a new item \nEnter (p) for plotting current items\n") == 'a':
        debt.add_a_debt()

    debt.plot_debt_over_all_period()


if __name__ == "__main__":
    main()
