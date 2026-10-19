"""Interactive command-line inventory and sales application."""

from inventory import Inventory
from reports import print_inventory, print_sales_report


def ask_int(prompt: str) -> int:
    """Read an integer safely from the terminal."""
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Please enter a whole number.")


def ask_float(prompt: str) -> float:
    """Read a numeric amount safely from the terminal."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0:
                print("Enter zero or a positive number.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def show_menu() -> None:
    print("\n===== INVENTORY & SALES MANAGER =====")
    print("1. Add product")
    print("2. List products")
    print("3. Search product")
    print("4. Restock product")
    print("5. Record sale")
    print("6. Show low-stock products")
    print("7. Show sales report")
    print("8. Exit")


def main() -> None:
    inventory = Inventory()

    while True:
        show_menu()
        choice = input("Choose 1-8: ").strip()

        if choice == "1":
            name = input("Product name: ").strip()
            sku = input("SKU/code: ").strip()
            price = ask_float("Unit price: ")
            quantity = ask_int("Opening quantity: ")
            threshold = ask_int("Low-stock threshold: ")
            try:
                product = inventory.add_product(
                    name, sku, price, quantity, threshold
                )
                print(f"Added {product['name']} (ID {product['id']}).")
            except ValueError as error:
                print(f"Could not add product: {error}")

        elif choice == "2":
            print_inventory(inventory.list_products())

        elif choice == "3":
            term = input("Search by name or SKU: ").strip()
            results = inventory.search_products(term)
            print_inventory(results)

        elif choice == "4":
            product_id = ask_int("Product ID: ")
            quantity = ask_int("Quantity to add: ")
            try:
                product = inventory.restock(product_id, quantity)
                print(
                    f"{product['name']} stock is now "
                    f"{product['quantity']}."
                )
            except (ValueError, KeyError) as error:
                print(f"Restock failed: {error}")

        elif choice == "5":
            product_id = ask_int("Product ID: ")
            quantity = ask_int("Quantity sold: ")
            try:
                sale = inventory.record_sale(product_id, quantity)
                print(
                    f"Sale #{sale['id']} recorded. "
                    f"Total: {sale['total']:.2f}"
                )
            except (ValueError, KeyError) as error:
                print(f"Sale failed: {error}")

        elif choice == "6":
            print_inventory(inventory.low_stock_products())

        elif choice == "7":
            print_sales_report(inventory.sales_summary())

        elif choice == "8":
            print("Data saved. Goodbye!")
            break

        else:
            print("Choose a valid option from 1 to 8.")


if __name__ == "__main__":
    main()
