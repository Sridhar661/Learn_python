
# Sales Analysis System
# 1
sales = [
    {"product": "Laptop", "quantity": 5, "price": 45000},
    {"product": "Mobile", "quantity": 10, "price": 15000},
    {"product": "Keyboard", "quantity": 20, "price": 800},
    {"product": "Mouse", "quantity": 30, "price": 500},
    {"product": "Monitor", "quantity": 8, "price": 12000},
    {"product": "Printer", "quantity": 4, "price": 9000},
    {"product": "Tablet", "quantity": 6, "price": 18000},
    {"product": "Headphones", "quantity": 15, "price": 2000},
]

def calculate_revenue():
    total = 0
    for item in sales:
        revenue = item["quantity"] * item["price"]
        total += revenue
    return total

def product_revenue():
    print("\nPRODUCT-WISE REVENUE")
    for item in sales:
        revenue = item["quantity"] * item["price"]
        print(item["product"], ":", revenue)

def total_quantity():
    quantity = sum(item["quantity"] for item in sales)
    print("Total units sold:", quantity)

def average_price():
    prices = [item["price"] for item in sales]
    average = sum(prices) / len(prices)
    print("Average product price:", round(average, 2))

def highest_revenue_product():
    product = max(sales, key=lambda x: x["quantity"] * x["price"])
    revenue = product["quantity"] * product["price"]
    print("Highest revenue product:", product["product"])
    print("Revenue:", revenue)

def lowest_revenue_product():
    product = min(sales, key=lambda x: x["quantity"] * x["price"])
    revenue = product["quantity"] * product["price"]
    print("Lowest revenue product:", product["product"])
    print("Revenue:", revenue)

def sort_by_revenue():
    sorted_sales = sorted(
        sales,
        key=lambda x: x["quantity"] * x["price"],
        reverse=True
    )
    print("\nRANKING BY REVENUE")
    for item in sorted_sales:
        revenue = item["quantity"] * item["price"]
        print(item["product"], ":", revenue)

def add_product():
    name = input("Product name: ")
    quantity = int(input("Quantity sold: "))
    price = float(input("Unit price: "))
    sales.append({
        "product": name,
        "quantity": quantity,
        "price": price
    })
    print("Product added!")

def search_product():
    name = input("Enter product name: ")
    found = False
    for item in sales:
        if item["product"].lower() == name.lower():
            print(item)
            found = True
    if not found:
        print("Product not found!")

def show_report():
    print("\n========== SALES REPORT ==========")
    print("Total revenue:", calculate_revenue())
    total_quantity()
    average_price()
    highest_revenue_product()
    lowest_revenue_product()
    print("==================================")

def main():
    while True:
        print("\n===== SALES ANALYTICS =====")
        print("1. Total Revenue")
        print("2. Product Revenue")
        print("3. Total Quantity")
        print("4. Average Price")
        print("5. Highest Revenue")
        print("6. Lowest Revenue")
        print("7. Sort Products")
        print("8. Add Product")
        print("9. Search Product")
        print("10. Complete Report")
        print("11. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print("Revenue:", calculate_revenue())
        elif choice == "2":
            product_revenue()
        elif choice == "3":
            total_quantity()
        elif choice == "4":
            average_price()
        elif choice == "5":
            highest_revenue_product()
        elif choice == "6":
            lowest_revenue_product()
        elif choice == "7":
            sort_by_revenue()
        elif choice == "8":
            add_product()
        elif choice == "9":
            search_product()
        elif choice == "10":
            show_report()
        elif choice == "11":
            print("Exiting Sales System...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
