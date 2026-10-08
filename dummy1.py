# ==============================
# Simple ATM System
# ==============================

balance = 10000.0
correct_pin = "1234"
transactions = []


def check_balance():
    print(f"\nCurrent Balance: ₹{balance:.2f}")


def deposit_money():
    global balance

    try:
        amount = float(input("Enter deposit amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        balance += amount
        transactions.append(f"Deposited ₹{amount:.2f}")

        print(f"₹{amount:.2f} deposited successfully.")
        print(f"New Balance: ₹{balance:.2f}")

    except ValueError:
        print("Please enter a valid number.")


def withdraw_money():
    global balance

    try:
        amount = float(input("Enter withdrawal amount: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        if amount > balance:
            print("Insufficient balance.")
            return

        balance -= amount
        transactions.append(f"Withdrawn ₹{amount:.2f}")

        print(f"Please collect ₹{amount:.2f}")
        print(f"Remaining Balance: ₹{balance:.2f}")

    except ValueError:
        print("Please enter a valid number.")


def show_transactions():
    print("\n----- TRANSACTIONS -----")

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(transaction)


def change_pin():
    global correct_pin

    old_pin = input("Enter your current PIN: ")

    if old_pin != correct_pin:
        print("Incorrect current PIN.")
        return

    new_pin = input("Enter your new 4-digit PIN: ")

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    correct_pin = new_pin
    print("PIN changed successfully.")


def show_menu():
    print("\n==========================")
    print("       ATM MENU")
    print("==========================")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Transaction History")
    print("5. Change PIN")
    print("6. Exit")
    print("==========================")


def login():
    attempts = 3

    while attempts > 0:
        entered_pin = input("Enter your PIN: ")

        if entered_pin == correct_pin:
            print("\nLogin successful!")
            return True

        attempts -= 1
        print(f"Incorrect PIN. Attempts left: {attempts}")

    print("Your card has been blocked.")
    return False


def main():
    print("==========================")
    print("   WELCOME TO PYTHON ATM")
    print("==========================")

    if not login():
        return

    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance()

        elif choice == "2":
            deposit_money()

        elif choice == "3":
            withdraw_money()

        elif choice == "4":
            show_transactions()

        elif choice == "5":
            change_pin()

        elif choice == "6":
            print("\nThank you for using Python ATM!")
            print("Please take your card.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()