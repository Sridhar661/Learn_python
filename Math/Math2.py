# Inventory Management System
# Python 3

import json
import os
from datetime import datetime

FILE_NAME = "inventory.json"


def load_inventory():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []


def save_inventory(inventory):
    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file, indent=4)


def display_products(inventory):
    print("\n========== PRODUCT INVENTORY ==========")
    if not inventory:
        print("No products available.")
        return

    for product in inventory:
        print(f"ID: {product['id']}")
        print(f"Name: {product['name']}")
        print(f"Price: Rs.{product['price']}")
        print(f"Quantity: {product['quantity']}")
        print("-" * 35)


def add_product(inventory):
    product_id = input("Enter product ID: ")

    if any(p["id"] == product_id for p in inventory):
        print("Product ID already exists.")
        return

    name = input("Enter product name: ")

    try:
        price = float(input("Enter product price: "))
        quantity = int(input("Enter quantity: "))

        if price < 0 or quantity < 0:
            print("Values cannot be negative.")
            return

    except ValueError:
        print("Invalid input.")
        return

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity,
        "created_at": datetime.now().isoformat()
    }

    inventory.append(product)
    save_inventory(inventory)
    print("Product added successfully!")


def search_product(inventory):
    search = input("Enter product name or ID: ").lower()

    results = [
        p for p in inventory
        if search in p["name"].lower()
        or search == p["id"].lower()
    ]

    if results:
        display_products(results)
    else:
        print("Product not found.")


def update_product(inventory):
    product_id = input("Enter product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            try:
                product["price"] = float(input("New price: "))
                product["quantity"] = int(input("New quantity: "))

                if product["price"] < 0 or product["quantity"] < 0:
                    raise ValueError

                save_inventory(inventory)
                print("Product updated successfully!")
            except ValueError:
                print("Invalid values.")
            return

    print("Product not found.")


def delete_product(inventory):
    product_id = input("Enter product ID: ")

    for product in inventory:
        if product["id"] == product_id:
            inventory.remove(product)
            save_inventory(inventory)
            print("Product deleted successfully!")
            return

    print("Product not found.")


def calculate_inventory_value(inventory):
    total = sum(
        p["price"] * p["quantity"]
        for p in inventory
    )

    print(f"Total inventory value: Rs.{total:.2f}")


def low_stock_report(inventory):
    print("\n========== LOW STOCK REPORT ==========")

    low_stock = [
        p for p in inventory
        if p["quantity"] < 10
    ]

    if not low_stock:
        print("No low-stock products.")
        return

    display_products(low_stock)


def main():
    inventory = load_inventory()

    while True:
        print("\n===== INVENTORY MANAGEMENT =====")
        print("1. Display Products")
        print("2. Add Product")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Inventory Value")
        print("7. Low Stock Report")
        print("8. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            display_products(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            search_product(inventory)
        elif choice == "4":
            update_product(inventory)
        elif choice == "5":
            delete_product(inventory)
        elif choice == "6":
            calculate_inventory_value(inventory)
        elif choice == "7":
            low_stock_report(inventory)
        elif choice == "8":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()