# ============================================================
# POINT OF SALE (POS) APPLICATION
# Product Management, Inventory, Billing, and Sales Reports
# ============================================================

from datetime import datetime

# Store application data in memory
products = {
    101: {"name": "Coca-Cola", "price": 40.0, "stock": 100},
    102: {"name": "Biscuits", "price": 20.0, "stock": 150},
    103: {"name": "Milk", "price": 30.0, "stock": 80},
    104: {"name": "Rice 1kg", "price": 65.0, "stock": 60},
    105: {"name": "Soap", "price": 35.0, "stock": 90},
}

sales_history = []
next_product_id = 106


def display_header(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50)


def display_products():
    display_header("PRODUCT INVENTORY")
    print(f"{'ID':<8}{'Product':<20}{'Price':<10}{'Stock':<8}")
    print("-" * 50)

    for product_id, product in products.items():
        print(
            f"{product_id:<8}"
            f"{product['name']:<20}"
            f"{product['price']:<10.2f}"
            f"{product['stock']:<8}"
        )


def add_product():
    global next_product_id

    display_header("ADD NEW PRODUCT")

    name = input("Enter product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Enter product price: "))
        stock = int(input("Enter initial stock: "))

        if price <= 0 or stock < 0:
            print("Price must be positive and stock cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid price and stock quantity.")
        return

    products[next_product_id] = {
        "name": name,
        "price": price,
        "stock": stock,
    }

    print(f"Product added successfully. ID: {next_product_id}")
    next_product_id += 1


def search_product():
    display_header("SEARCH PRODUCT")

    keyword = input("Enter product name or ID: ").strip().lower()

    found = False

    for product_id, product in products.items():
        if (
            keyword == str(product_id)
            or keyword in product["name"].lower()
        ):
            print(
                f"ID: {product_id} | "
                f"Name: {product['name']} | "
                f"Price: Rs.{product['price']:.2f} | "
                f"Stock: {product['stock']}"
            )
            found = True

    if not found:
        print("No matching product found.")


def restock_product():
    display_header("RESTOCK INVENTORY")

    try:
        product_id = int(input("Enter product ID: "))
        quantity = int(input("Enter quantity to add: "))

        if product_id not in products:
            print("Product not found.")
            return

        if quantity <= 0:
            print("Quantity must be positive.")
            return

        products[product_id]["stock"] += quantity

        print(
            f"Stock updated. New stock: "
            f"{products[product_id]['stock']}"
        )

    except ValueError:
        print("Enter valid numeric values.")


def generate_bill():
    display_header("CUSTOMER BILLING")

    cart = {}

    while True:
        display_products()

        try:
            product_id = int(
                input("\nEnter product ID (0 to finish): ")
            )

            if product_id == 0:
                break

            if product_id not in products:
                print("Invalid product ID.")
                continue

            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Quantity must be positive.")
                continue

            available = (
                products[product_id]["stock"]
                - cart.get(product_id, 0)
            )

            if quantity > available:
                print(f"Only {available} units available.")
                continue

            cart[product_id] = cart.get(product_id, 0) + quantity
            print("Product added to cart.")

        except ValueError:
            print("Please enter valid numbers.")

    if not cart:
        print("Cart is empty. No bill generated.")
        return

    subtotal = 0.0
    bill_items = []

    print("\n" + "=" * 50)
    print("                 CUSTOMER BILL")
    print("=" * 50)
    print("Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 50)

    for product_id, quantity in cart.items():
        product = products[product_id]
        amount = product["price"] * quantity
        subtotal += amount

        bill_items.append({
            "product_id": product_id,
            "name": product["name"],
            "quantity": quantity,
            "unit_price": product["price"],
            "amount": amount,
        })

        print(
            f"{product['name']:<18} "
            f"{quantity:>3} x "
            f"Rs.{product['price']:.2f} = "
            f"Rs.{amount:.2f}"
        )

    tax = subtotal * 0.05
    total = subtotal + tax

    print("-" * 50)
    print(f"Subtotal: Rs.{subtotal:.2f}")
    print(f"Tax (5% demo): Rs.{tax:.2f}")
    print(f"Total: Rs.{total:.2f}")

    confirm = input("Confirm sale? (yes/no): ").strip().lower()

    if confirm != "yes":
        print("Sale cancelled. Stock remains unchanged.")
        return

    # Update stock only after the sale is confirmed.
    for product_id, quantity in cart.items():
        products[product_id]["stock"] -= quantity

    sale = {
        "sale_id": len(sales_history) + 1,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": bill_items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }

    sales_history.append(sale)

    print("=" * 50)
    print("Sale completed successfully!")
    print(f"Bill Number: {sale['sale_id']}")
    print("=" * 50)


def view_sales_report():
    display_header("SALES REPORT")

    if not sales_history:
        print("No sales recorded yet.")
        return

    total_revenue = 0.0
    total_transactions = len(sales_history)
    total_units_sold = 0

    for sale in sales_history:
        total_revenue += sale["total"]

        for item in sale["items"]:
            total_units_sold += item["quantity"]

    print(f"Total transactions: {total_transactions}")
    print(f"Total units sold: {total_units_sold}")
    print(f"Total revenue: Rs.{total_revenue:.2f}")

    print("\nTransaction Details")
    print("-" * 50)

    for sale in sales_history:
        print(
            f"Bill #{sale['sale_id']} | "
            f"{sale['date']} | "
            f"Rs.{sale['total']:.2f}"
        )


def low_stock_report():
    display_header("LOW STOCK ALERT")

    threshold = 20
    low_stock_found = False

    for product_id, product in products.items():
        if product["stock"] <= threshold:
            print(
                f"ALERT: {product['name']} "
                f"has only {product['stock']} units left."
            )
            low_stock_found = True

    if not low_stock_found:
        print("All products have sufficient stock.")


def main():
    while True:
        display_header("PYTHON POS MANAGEMENT SYSTEM")

        print("1. View Products")
        print("2. Add Product")
        print("3. Search Product")
        print("4. Restock Inventory")
        print("5. Generate Customer Bill")
        print("6. View Sales Report")
        print("7. Low Stock Alert")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            display_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            search_product()
        elif choice == "4":
            restock_product()
        elif choice == "5":
            generate_bill()
        elif choice == "6":
            view_sales_report()
        elif choice == "7":
            low_stock_report()
        elif choice == "8":
            print("Thank you for using the POS application!")
            break
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    main()