
# ==========================================
# BANKING MANAGEMENT SYSTEM
# ==========================================

import random
from datetime import datetime


class BankAccount:

    def __init__(self, name, initial_balance=0):
        self.account_number = random.randint(100000, 999999)
        self.name = name
        self.balance = initial_balance
        self.transactions = []

        self.add_transaction("Account Created", initial_balance)

    def add_transaction(self, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.transactions.append(transaction)

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount!")
            return

        self.balance += amount
        self.add_transaction("Deposit", amount)

        print("Deposit successful!")
        print("Current Balance:", self.balance)

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount!")
            return

        if amount > self.balance:
            print("Insufficient balance!")
            return

        self.balance -= amount
        self.add_transaction("Withdrawal", amount)

        print("Withdrawal successful!")
        print("Current Balance:", self.balance)

    def check_balance(self):
        print("\nAccount Holder:", self.name)
        print("Account Number:", self.account_number)
        print("Available Balance:", self.balance)

    def transfer(self, receiver, amount):
        if amount <= 0:
            print("Invalid amount!")
            return

        if amount > self.balance:
            print("Insufficient balance!")
            return

        self.balance -= amount
        receiver.balance += amount

        self.add_transaction("Transfer Sent", amount)
        receiver.add_transaction("Transfer Received", amount)

        print("Transfer successful!")

    def transaction_history(self):
        print("\n--- Transaction History ---")

        if not self.transactions:
            print("No transactions found.")
            return

        for transaction in self.transactions:
            print("-" * 40)
            print("Type:", transaction["type"])
            print("Amount:", transaction["amount"])
            print("Date:", transaction["date"])


class Bank:

    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter Account Holder Name: ")

        try:
            balance = float(input("Initial Deposit: "))

            if balance < 0:
                print("Balance cannot be negative.")
                return

            account = BankAccount(name, balance)

            self.accounts[account.account_number] = account

            print("\nAccount Created Successfully!")
            print("Your Account Number:", account.account_number)

        except ValueError:
            print("Invalid amount!")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def deposit_money(self):
        try:
            account_number = int(input("Account Number: "))
            account = self.get_account(account_number)

            if account:
                amount = float(input("Deposit Amount: "))
                account.deposit(amount)
            else:
                print("Account not found.")

        except ValueError:
            print("Invalid input!")

    def withdraw_money(self):
        try:
            account_number = int(input("Account Number: "))
            account = self.get_account(account_number)

            if account:
                amount = float(input("Withdrawal Amount: "))
                account.withdraw(amount)
            else:
                print("Account not found.")

        except ValueError:
            print("Invalid input!")

    def transfer_money(self):
        try:
            sender_number = int(input("Sender Account: "))
            receiver_number = int(input("Receiver Account: "))

            sender = self.get_account(sender_number)
            receiver = self.get_account(receiver_number)

            if not sender or not receiver:
                print("Invalid account number.")
                return

            if sender == receiver:
                print("Cannot transfer to the same account.")
                return

            amount = float(input("Transfer Amount: "))
            sender.transfer(receiver, amount)

        except ValueError:
            print("Invalid input!")

    def check_account(self):
        try:
            account_number = int(input("Account Number: "))
            account = self.get_account(account_number)

            if account:
                account.check_balance()
            else:
                print("Account not found.")

        except ValueError:
            print("Invalid account number!")

    def show_history(self):
        try:
            account_number = int(input("Account Number: "))
            account = self.get_account(account_number)

            if account:
                account.transaction_history()
            else:
                print("Account not found.")

        except ValueError:
            print("Invalid account number!")

    def show_all_accounts(self):
        print("\n--- All Bank Accounts ---")

        for account in self.accounts.values():
            account.check_balance()

    def run(self):
        while True:
            print("\n========== BANK MANAGEMENT ==========")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. Check Balance")
            print("6. Transaction History")
            print("7. All Accounts")
            print("8. Exit")

            choice = input("Choose Option: ")

            if choice == "1":
                self.create_account()

            elif choice == "2":
                self.deposit_money()

            elif choice == "3":
                self.withdraw_money()

            elif choice == "4":
                self.transfer_money()

            elif choice == "5":
                self.check_account()

            elif choice == "6":
                self.show_history()

            elif choice == "7":
                self.show_all_accounts()

            elif choice == "8":
                print("Thank you for using our bank!")
                break

            else:
                print("Invalid choice!")


if __name__ == "__main__":
    bank = Bank()
    bank.run()
