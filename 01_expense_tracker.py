"""A beginner-friendly command-line expense tracker."""
from datetime import date
from pathlib import Path
import csv

DATA_FILE = Path("expenses.csv")
CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Other"]


def load_expenses():
    """Load saved expenses from the CSV file."""
    expenses = []
    if not DATA_FILE.exists():
        return expenses
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


def save_expenses(expenses):
    """Save all expenses to the CSV file."""
    with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
        fields = ["day", "category", "description", "amount"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(expenses)


def add_expense(expenses):
    """Ask the user for details and add one expense."""
    print("\nCategories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    if category not in CATEGORIES:
        print("Unknown category. Using Other.")
        category = "Other"
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount: "))
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Enter a positive number.")
        return
    expenses.append({"day": date.today().isoformat(),
                     "category": category, "description": description,
                     "amount": amount})
    save_expenses(expenses)
    print("Expense saved.")


def show_expenses(expenses):
    """Display all recorded expenses."""
    print("\nDATE        CATEGORY    DESCRIPTION              AMOUNT")
    print("-" * 65)
    for item in expenses:
        print(f"{item['day']:<11}{item['category']:<12}"
              f"{item['description']:<25}{item['amount']:>8.2f}")
    if not expenses:
        print("No expenses recorded yet.")


def show_summary(expenses):
    """Display total spending grouped by category."""
    totals = {}
    for item in expenses:
        category = item["category"]
        totals[category] = totals.get(category, 0) + item["amount"]
    print("\nSPENDING SUMMARY")
    print("-" * 30)
    for category, total in sorted(totals.items()):
        print(f"{category:<15} {total:>10.2f}")
    print("-" * 30)
    print(f"{'TOTAL':<15} {sum(totals.values()):>10.2f}")


def main():
    """Run the expense tracker menu."""
    expenses = load_expenses()
    while True:
        print("\n=== EXPENSE TRACKER ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Category summary")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            show_summary(expenses)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try 1 to 4.")


