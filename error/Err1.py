
import json
import logging
import math
import os
import sys
import unittest
from datetime import datetime
from pathlib import Path

# ============================================================
# BANKING EXCEPTION HANDLING PROJECT
# ============================================================

APP_NAME = "Python Banking Practice Application"
DATA_FILE = Path("bank_data.json")
LOG_FILE = Path("bank_errors.log")

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# ============================================================
# CUSTOM EXCEPTIONS
# ============================================================

class BankingError(Exception):
    """Base exception for banking errors."""
    pass


class InvalidAmountError(BankingError):
    """Raised when an amount is invalid."""
    pass


class InsufficientBalanceError(BankingError):
    """Raised when the balance is insufficient."""
    pass


class AccountNotFoundError(BankingError):
    """Raised when an account cannot be found."""
    pass


class DuplicateAccountError(BankingError):
    """Raised when an account already exists."""
    pass


class InvalidAccountError(BankingError):
    """Raised when account details are invalid."""
    pass


class DataStorageError(BankingError):
    """Raised when stored data cannot be accessed."""
    pass


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_name(name):
    try:
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")

        name = name.strip()

        if not name:
            raise ValueError("Name cannot be empty.")

        if len(name) < 2:
            raise ValueError("Name must have at least 2 characters.")

        return name

    except (TypeError, ValueError):
        raise


def validate_account_number(account_number):
    try:
        if not isinstance(account_number, str):
            raise TypeError("Account number must be text.")

        account_number = account_number.strip()

        if not account_number:
            raise ValueError("Account number cannot be empty.")

        if not account_number.isdigit():
            raise ValueError("Account number must contain digits.")

        return account_number

    except (TypeError, ValueError):
        raise


def validate_amount(amount):
    try:
        amount = float(amount)

        if not math.isfinite(amount):
            raise InvalidAmountError(
                "Amount must be a finite number."
            )

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than zero."
            )

        return round(amount, 2)

    except (ValueError, TypeError) as error:
        raise InvalidAmountError(
            "Please enter a valid numeric amount."
        ) from error


def validate_pin(pin):
    try:
        pin = str(pin)

        if len(pin) != 4 or not pin.isdigit():
            raise ValueError(
                "PIN must contain exactly four digits."
            )

        return pin

    except (TypeError, ValueError):
        raise


# ============================================================
# ACCOUNT CLASS
# ============================================================

class Account:
    def __init__(
        self,
        account_number,
        owner_name,
        balance=0.0,
        pin="1234"
    ):
        self.account_number = validate_account_number(
            account_number
        )
        self.owner_name = validate_name(owner_name)
        self.balance = validate_amount(balance) if balance else 0.0
        self.pin = validate_pin(pin)
        self.created_at = datetime.now().isoformat()
        self.transactions = []

    def add_transaction(self, transaction_type, amount):
        transaction = {
            "type": transaction_type,
            "amount": round(amount, 2),
            "balance": round(self.balance, 2),
            "time": datetime.now().isoformat()
        }
        self.transactions.append(transaction)

    def deposit(self, amount):
        amount = validate_amount(amount)
        self.balance = round(self.balance + amount, 2)
        self.add_transaction("DEPOSIT", amount)
        return self.balance

    def withdraw(self, amount):
        amount = validate_amount(amount)

        if amount > self.balance:
            raise InsufficientBalanceError(
                "Insufficient balance for withdrawal."
            )

        self.balance = round(self.balance - amount, 2)
        self.add_transaction("WITHDRAWAL", amount)
        return self.balance

    def transfer_to(self, target_account, amount):
        amount = validate_amount(amount)

        if not isinstance(target_account, Account):
            raise InvalidAccountError(
                "Target must be a valid account."
            )

        if target_account is self:
            raise InvalidAccountError(
                "Cannot transfer to the same account."
            )

        if amount > self.balance:
            raise InsufficientBalanceError(
                "Insufficient balance for transfer."
            )

        self.balance = round(self.balance - amount, 2)
        target_account.balance = round(
            target_account.balance + amount, 2
        )

        self.add_transaction("TRANSFER_OUT", amount)
        target_account.add_transaction("TRANSFER_IN", amount)

    def check_pin(self, pin):
        return self.pin == str(pin)

    def get_statement(self):
        return list(self.transactions)

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "owner_name": self.owner_name,
            "balance": self.balance,
            "pin": self.pin,
            "created_at": self.created_at,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        account = cls(
            account_number=data["account_number"],
            owner_name=data["owner_name"],
            balance=data["balance"],
            pin=data["pin"]
        )
        account.created_at = data.get(
            "created_at", datetime.now().isoformat()
        )
        account.transactions = data.get("transactions", [])
        return account


# ============================================================
# BANK CLASS
# ============================================================

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(
        self,
        account_number,
        owner_name,
        initial_balance=0.0,
        pin="1234"
    ):
        account_number = validate_account_number(account_number)

        if account_number in self.accounts:
            raise DuplicateAccountError(
                "Account already exists."
            )

        account = Account(
            account_number,
            owner_name,
            initial_balance,
            pin
        )

        self.accounts[account_number] = account
        return account

    def get_account(self, account_number):
        account_number = validate_account_number(account_number)

        try:
            return self.accounts[account_number]
        except KeyError as error:
            raise AccountNotFoundError(
                "Account does not exist."
            ) from error

    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        return account.deposit(amount)

    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        return account.withdraw(amount)

    def transfer(self, source_number, target_number, amount):
        source = self.get_account(source_number)
        target = self.get_account(target_number)
        source.transfer_to(target, amount)

    def list_accounts(self):
        return list(self.accounts.values())

    def total_money(self):
        return round(
            sum(account.balance for account in self.accounts.values()),
            2
        )

    def to_dict(self):
        return {
            number: account.to_dict()
            for number, account in self.accounts.items()
        }

    def load_dict(self, data):
        if not isinstance(data, dict):
            raise DataStorageError(
                "Stored bank data must be a dictionary."
            )

        accounts = {}

        try:
            for number, account_data in data.items():
                account = Account.from_dict(account_data)

                if account.account_number != number:
                    raise DataStorageError(
                        "Account number mismatch in stored data."
                    )

                accounts[number] = account

        except (KeyError, TypeError, ValueError, BankingError) as error:
            raise DataStorageError(
                "Stored account data is invalid."
            ) from error

        self.accounts = accounts


# ============================================================
# JSON STORAGE
# ============================================================

def save_bank(bank, filename=DATA_FILE):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(bank.to_dict(), file, indent=4)

    except (OSError, TypeError, ValueError) as error:
        logging.exception("Failed to save bank data.")
        raise DataStorageError(
            "Could not save bank data."
        ) from error

    else:
        print("Bank data saved successfully.")

    finally:
        print("Save operation finished.")


def load_bank(filename=DATA_FILE):
    bank = Bank()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        bank.load_dict(data)

    except FileNotFoundError:
        print("No saved data found. Starting with an empty bank.")

    except json.JSONDecodeError as error:
        logging.exception("Invalid JSON data.")
        raise DataStorageError(
            "Bank data file contains invalid JSON."
        ) from error

    except OSError as error:
        logging.exception("Could not read bank data.")
        raise DataStorageError(
            "Could not read bank data."
        ) from error

    return bank


# ============================================================
# SAFE INPUT FUNCTIONS
# ============================================================

def read_text(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
        raise


def read_amount(prompt):
    while True:
        try:
            value = input(prompt)
            return validate_amount(value)

        except InvalidAmountError as error:
            print("Input error:", error)

        except (EOFError, KeyboardInterrupt):
            raise


def read_account_number(prompt):
    while True:
        try:
            value = input(prompt)
            return validate_account_number(value)

        except (TypeError, ValueError) as error:
            print("Account error:", error)

        except (EOFError, KeyboardInterrupt):
            raise


def read_pin(prompt="Enter four-digit PIN: "):
    while True:
        try:
            value = input(prompt)
            return validate_pin(value)

        except (TypeError, ValueError) as error:
            print("PIN error:", error)

        except (EOFError, KeyboardInterrupt):
            raise


def authenticate(account):
    try:
        pin = input("Enter your PIN: ")

        if not account.check_pin(pin):
            raise PermissionError("Incorrect PIN.")

        return True

    except PermissionError as error:
        print("Authentication failed:", error)
        return False


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def display_account(account):
    print("\n------------------------------")
    print("Account number:", account.account_number)
    print("Account holder:", account.owner_name)
    print("Balance: Rs.", f"{account.balance:.2f}")
    print("Created:", account.created_at)
    print("------------------------------")


def display_transactions(account):
    transactions = account.get_statement()

    if not transactions:
        print("No transactions found.")
        return

    print("\nTRANSACTION STATEMENT")

    for index, transaction in enumerate(transactions, start=1):
        print("Transaction:", index)
        print("Type:", transaction["type"])
        print("Amount:", transaction["amount"])
        print("Balance:", transaction["balance"])
        print("Time:", transaction["time"])
        print("------------------------------")


def display_all_accounts(bank):
    accounts = bank.list_accounts()

    if not accounts:
        print("No accounts available.")
        return

    for account in accounts:
        display_account(account)

    print("Total bank balance:", bank.total_money())


# ============================================================
# BANKING OPERATIONS
# ============================================================

def create_account_menu(bank):
    try:
        number = read_account_number("Account number: ")
        name = read_text("Account holder name: ")
        pin = read_pin()
        initial = input("Initial deposit (default 0): ").strip()
        initial_balance = 0.0 if initial == "" else validate_amount(initial)

        account = bank.create_account(
            number, name, initial_balance, pin
        )

        print("Account created successfully.")
        display_account(account)

    except DuplicateAccountError as error:
        print("Creation error:", error)

    except (ValueError, TypeError, BankingError) as error:
        print("Invalid account details:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nAccount creation cancelled.")


def deposit_menu(bank):
    try:
        number = read_account_number("Account number: ")
        account = bank.get_account(number)

        if not authenticate(account):
            return

        amount = read_amount("Deposit amount: ")
        balance = bank.deposit(number, amount)
        print("Deposit successful.")
        print("New balance:", balance)

    except (BankingError, ValueError) as error:
        print("Deposit failed:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nDeposit cancelled.")


def withdraw_menu(bank):
    try:
        number = read_account_number("Account number: ")
        account = bank.get_account(number)

        if not authenticate(account):
            return

        amount = read_amount("Withdrawal amount: ")
        balance = bank.withdraw(number, amount)
        print("Withdrawal successful.")
        print("Remaining balance:", balance)

    except InsufficientBalanceError as error:
        print("Withdrawal rejected:", error)

    except BankingError as error:
        print("Withdrawal failed:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nWithdrawal cancelled.")


def transfer_menu(bank):
    try:
        source_number = read_account_number("Your account number: ")
        source = bank.get_account(source_number)

        if not authenticate(source):
            return

        target_number = read_account_number(
            "Receiver account number: "
        )
        amount = read_amount("Transfer amount: ")

        bank.transfer(source_number, target_number, amount)

        print("Transfer completed successfully.")

    except InsufficientBalanceError as error:
        print("Transfer rejected:", error)

    except BankingError as error:
        print("Transfer failed:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nTransfer cancelled.")


def statement_menu(bank):
    try:
        number = read_account_number("Account number: ")
        account = bank.get_account(number)

        if authenticate(account):
            display_transactions(account)

    except BankingError as error:
        print("Statement unavailable:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nStatement request cancelled.")


def balance_menu(bank):
    try:
        number = read_account_number("Account number: ")
        account = bank.get_account(number)

        if authenticate(account):
            display_account(account)

    except BankingError as error:
        print("Balance request failed:", error)

    except (EOFError, KeyboardInterrupt):
        print("\nBalance request cancelled.")


# ============================================================
# EXCEPTION DEMONSTRATIONS
# ============================================================

def demonstrate_zero_division():
    try:
        numerator = 100
        denominator = 0
        print(numerator / denominator)

    except ZeroDivisionError as error:
        print("Caught ZeroDivisionError:", error)


def demonstrate_value_error():
    try:
        number = int("hello")
        print(number)

    except ValueError as error:
        print("Caught ValueError:", error)


def demonstrate_type_error():
    try:
        result = "Python" + 10
        print(result)

    except TypeError as error:
        print("Caught TypeError:", error)


def demonstrate_index_error():
    try:
        numbers = [10, 20, 30]
        print(numbers[10])

    except IndexError as error:
        print("Caught IndexError:", error)


def demonstrate_key_error():
    try:
        student = {"name": "Ravi"}
        print(student["marks"])

    except KeyError as error:
        print("Caught KeyError:", error)


def demonstrate_name_error():
    try:
        print(undefined_variable)

    except NameError as error:
        print("Caught NameError:", error)


def demonstrate_file_error():
    try:
        with open("missing_file.txt", "r") as file:
            print(file.read())

    except FileNotFoundError as error:
        print("Caught FileNotFoundError:", error)


def demonstrate_custom_exception():
    try:
        amount = -100

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be positive."
            )

    except InvalidAmountError as error:
        print("Caught custom exception:", error)


def demonstrate_else_finally():
    try:
        number = 20
        result = number / 4

    except ZeroDivisionError:
        print("Division failed.")

    else:
        print("Calculation succeeded:", result)

    finally:
        print("Execution finished.")


def run_exception_demos():
    print("\nEXCEPTION DEMONSTRATIONS")

    demonstrate_zero_division()
    demonstrate_value_error()
    demonstrate_type_error()
    demonstrate_index_error()
    demonstrate_key_error()
    demonstrate_name_error()
    demonstrate_file_error()
    demonstrate_custom_exception()
    demonstrate_else_finally()


# ============================================================
# UNIT TESTS
# ============================================================

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(
            "1001", "Test User", 1000, "1234"
        )

    def test_account_creation(self):
        self.assertEqual(
            self.account.account_number, "1001"
        )

    def test_initial_balance(self):
        self.assertEqual(self.account.balance, 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_withdraw(self):
        self.account.withdraw(200)
        self.assertEqual(self.account.balance, 800)

    def test_zero_deposit(self):
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(0)

    def test_negative_deposit(self):
        with self.assertRaises(InvalidAmountError):
            self.account.deposit(-100)

    def test_insufficient_balance(self):
        with self.assertRaises(InsufficientBalanceError):
            self.account.withdraw(2000)

    def test_invalid_pin(self):
        self.assertFalse(self.account.check_pin("9999"))

    def test_correct_pin(self):
        self.assertTrue(self.account.check_pin("1234"))

    def test_transaction_recorded(self):
        self.account.deposit(100)
        self.assertEqual(len(self.account.transactions), 1)

    def test_transfer(self):
        target = Account("1002", "Receiver", 100, "5678")
        self.account.transfer_to(target, 200)
        self.assertEqual(self.account.balance, 800)
        self.assertEqual(target.balance, 300)


class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.bank.create_account("1001", "Alice", 1000, "1234")
        self.bank.create_account("1002", "Bob", 500, "5678")

    def test_create_account(self):
        account = self.bank.create_account(
            "1003", "Charlie", 100, "2222"
        )
        self.assertEqual(account.balance, 100)

    def test_duplicate_account(self):
        with self.assertRaises(DuplicateAccountError):
            self.bank.create_account("1001", "Other", 100, "1111")

    def test_missing_account(self):
        with self.assertRaises(AccountNotFoundError):
            self.bank.get_account("9999")

    def test_deposit(self):
        self.bank.deposit("1001", 200)
        self.assertEqual(self.bank.get_account("1001").balance, 1200)

    def test_withdraw(self):
        self.bank.withdraw("1001", 200)
        self.assertEqual(self.bank.get_account("1001").balance, 800)

    def test_transfer(self):
        self.bank.transfer("1001", "1002", 300)
        self.assertEqual(self.bank.get_account("1001").balance, 700)
        self.assertEqual(self.bank.get_account("1002").balance, 800)

    def test_total_money(self):
        self.assertEqual(self.bank.total_money(), 1500)


# ============================================================
# MAIN MENU
# ============================================================

def show_menu():
    print("\n================================")
    print(APP_NAME)
    print("================================")
    print("1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Check balance")
    print("6. View statement")
    print("7. Display all accounts")
    print("8. Run exception demonstrations")
    print("9. Save bank data")
    print("10. Exit")
    print("================================")


def main():
    try:
        bank = load_bank()

    except DataStorageError as error:
        print("Storage error:", error)
        print("Please inspect the data file before continuing.")
        return

    while True:
        try:
            show_menu()
            choice = input("Choose an option: ").strip()

            if choice == "1":
                create_account_menu(bank)

            elif choice == "2":
                deposit_menu(bank)

            elif choice == "3":
                withdraw_menu(bank)

            elif choice == "4":
                transfer_menu(bank)

            elif choice == "5":
                balance_menu(bank)

            elif choice == "6":
                statement_menu(bank)

            elif choice == "7":
                display_all_accounts(bank)

            elif choice == "8":
                run_exception_demos()

            elif choice == "9":
                save_bank(bank)

            elif choice == "10":
                save_bank(bank)
                print("Thank you for using the application.")
                break

            else:
                print("Invalid choice. Enter 1 to 10.")

        except (EOFError, KeyboardInterrupt):
            print("\nExiting application.")
            break

        except Exception:
            logging.exception("Unexpected application error.")
            print("Unexpected error. Check the application log.")

        finally:
            pass


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    if "--test" in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        main()







        
"""Basic calculator utilities with input validation."""

import math


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b


def power(base: float, exponent: float) -> float:
    return base ** exponent


def square_root(number: float) -> float:
    if number < 0:
        raise ValueError("Cannot calculate a real square root of a negative number.")
    return math.sqrt(number)


def percentage(value: float, total: float) -> float:
    if total == 0:
        raise ZeroDivisionError("Total cannot be zero.")
    return value / total * 100


def factorial(number: int) -> int:
    if not isinstance(number, int) or isinstance(number, bool):
        raise TypeError("Number must be an integer.")
    if number < 0:
        raise ValueError("Number cannot be negative.")
    return math.factorial(number)


def average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate the average of an empty list.")
    return sum(numbers) / len(numbers)


def maximum(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("List cannot be empty.")
    return max(numbers)


def minimum(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("List cannot be empty.")
    return min(numbers)


if __name__ == "__main__":
    print("Addition:", add(10, 20))
    print("Division:", divide(100, 5))
    print("Square root:", square_root(144))
    print("Percentage:", percentage(45, 60))
    print("Average:", average([10, 20, 30, 40]))
```

Create `exception_handler.py`:

<CodeBlock language="python" editable>
"""Reusable exception-handling examples."""


def safe_integer(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def safe_division(a: float, b: float) -> dict:
    try:
        result = a / b
    except ZeroDivisionError as error:
        return {"success": False, "error": str(error)}
    else:
        return {"success": True, "result": result}
    finally:
        # Useful for cleanup or tracking operation completion.
        pass


def validate_positive(number: float) -> float:
    if number <= 0:
        raise ValueError("Number must be positive.")
    return number


def read_file(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as file:
            return {"success": True, "content": file.read()}
    except FileNotFoundError:
        return {"success": False, "error": "File not found."}
    except PermissionError:
        return {"success": False, "error": "Permission denied."}
    except OSError as error:
        return {"success": False, "error": str(error)}
```

Create `test_calculator.py`:

<CodeBlock language="python" editable>
"""Tests for calculator functions."""

import unittest

from calculator import (
    add,
    subtract,
    multiply,
    divide,
    square_root,
    percentage,
    factorial,
    average,
)


class CalculatorTests(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(10, 20), 30)

    def test_subtract(self):
        self.assertEqual(subtract(20, 5), 15)

    def test_multiply(self):
        self.assertEqual(multiply(4, 5), 20)

    def test_divide(self):
        self.assertEqual(divide(20, 4), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)

    def test_square_root(self):
        self.assertEqual(square_root(81), 9)

    def test_negative_square_root(self):
        with self.assertRaises(ValueError):
            square_root(-1)

    def test_percentage(self):
        self.assertEqual(percentage(25, 100), 25)

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)

    def test_negative_factorial(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_average(self):
        self.assertEqual(average([10, 20, 30]), 20)

    def test_empty_average(self):
        with self.assertRaises(ValueError):
            average([])


if __name__ == "__main__":
    unittest.main()

