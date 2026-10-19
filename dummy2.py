
# Mini POS Billing System
# Single-file Python project

products = {
    101: {"name": "Rice", "price": 60.0, "stock": 100},
    102: {"name": "Sugar", "price": 45.0, "stock": 80},
    103: {"name": "Milk", "price": 30.0, "stock": 50},
    104: {"name": "Coffee", "price": 120.0, "stock": 40},
    105: {"name": "Soap", "price": 35.0, "stock": 60},
}

sales_history = []


def display_products():
    print("\n========== PRODUCT LIST ==========")
    print(f"{'ID':<8}{'Name':<15}{'Price':<12}{'Stock':<10}")

    for product_id, product in products.items():
        print(
            f"{product_id:<8}"
            f"{product['name']:<15}"
            f"{product['price']:<12.2f}"
            f"{product['stock']:<10}"
        )


def add_product():
    try:
        product_id = int(input("Enter product ID: "))

        if product_id in products:
            print("Product ID already exists!")
            return

        name = input("Enter product name: ").strip()
        price = float(input("Enter product price: "))
        stock = int(input("Enter stock quantity: "))

        if not name or price < 0 or stock < 0:
            print("Invalid product details!")
            return

        products[product_id] = {
            "name": name,
            "price": price,
            "stock": stock,
        }

        print("Product added successfully!")

    except ValueError:
        print("Please enter valid numeric values.")


def restock_product():
    try:
        product_id = int(input("Enter product ID: "))

        if product_id not in products:
            print("Product not found!")
            return

        quantity = int(input("Enter quantity to add: "))

        if quantity <= 0:
            print("Quantity must be positive.")
            return

        products[product_id]["stock"] += quantity
        print("Stock updated successfully!")

    except ValueError:
        print("Invalid input!")


def create_bill():
    cart = {}
    print("\nEnter product IDs to add to the cart.")
    print("Enter 0 when you finish shopping.")

    while True:
        try:
            product_id = int(input("Product ID: "))

            if product_id == 0:
                break

            if product_id not in products:
                print("Product not found!")
                continue

            quantity = int(input("Quantity: "))

            if quantity <= 0:
                print("Quantity must be positive.")
                continue

            available = products[product_id]["stock"]
            already_added = cart.get(product_id, 0)

            if quantity + already_added > available:
                print(f"Only {available - already_added} more available.")
                continue

            cart[product_id] = already_added + quantity

        except ValueError:
            print("Enter valid numbers.")

    if not cart:
        print("Cart is empty.")
        return

    subtotal = sum(
        products[pid]["price"] * qty
        for pid, qty in cart.items()
    )

    discount_rate = 0.05 if subtotal >= 1000 else 0
    discount = subtotal * discount_rate
    taxable_amount = subtotal - discount
    gst_rate = 0.05
    gst = taxable_amount * gst_rate
    total = taxable_amount + gst

    print("\n============= CUSTOMER BILL =============")

    for pid, qty in cart.items():
        product = products[pid]
        amount = product["price"] * qty
        print(f"{product['name']:<15} x {qty:<3} Rs. {amount:.2f}")

    print("-----------------------------------------")
    print(f"Subtotal:             Rs. {subtotal:.2f}")
    print(f"Discount:             Rs. {discount:.2f}")
    print(f"GST (5% demo):        Rs. {gst:.2f}")
    print(f"Total:                Rs. {total:.2f}")

    payment = input("Payment (cash/card/upi): ").strip().lower()

    if payment not in ["cash", "card", "upi"]:
        print("Invalid payment method. Bill cancelled.")
        return

    for pid, qty in cart.items():
        products[pid]["stock"] -= qty

    sales_history.append({
        "subtotal": subtotal,
        "discount": discount,
        "gst": gst,
        "total": total,
        "payment": payment,
    })

    print(f"Payment successful using {payment.upper()}!")
    print("Thank you for shopping!")


def low_stock_report():
    print("\n========== LOW STOCK REPORT ==========")
    found = False

    for pid, product in products.items():
        if product["stock"] <= 10:
            print(
                f"{pid} - {product['name']} "
                f"- Remaining: {product['stock']}"
            )
            found = True

    if not found:
        print("No products have low stock.")


def sales_report():
    print("\n========== SALES REPORT ==========")

    if not sales_history:
        print("No sales recorded.")
        return

    total_revenue = sum(
        sale["total"] for sale in sales_history
    )

    print(f"Number of bills: {len(sales_history)}")
    print(f"Total revenue: Rs. {total_revenue:.2f}")

    for method in ["cash", "card", "upi"]:
        amount = sum(
            sale["total"]
            for sale in sales_history
            if sale["payment"] == method
        )
        print(f"{method.upper()} sales: Rs. {amount:.2f}")


def main():
    while True:
        print("\n========== MINI POS SYSTEM ==========")
        print("1. Display Products")
        print("2. Add Product")
        print("3. Restock Product")
        print("4. Create Bill")
        print("5. Low Stock Report")
        print("6. Sales Report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            restock_product()
        elif choice == "4":
            create_bill()
        elif choice == "5":
            low_stock_report()
        elif choice == "6":
            sales_report()
        elif choice == "7":
            print("POS system closed.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()