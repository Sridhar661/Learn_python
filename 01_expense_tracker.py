
# ==========================================
# SUPPLY CHAIN MANAGEMENT SYSTEM
# ==========================================

from datetime import datetime
import random


# ------------------------------------------
# PRODUCT CLASS
# ------------------------------------------

class Product:

    def __init__(self, product_id, name, price, quantity):

        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def display_product(self):

        print("\nProduct ID:", self.product_id)
        print("Product Name:", self.name)
        print("Price:", self.price)
        print("Available Stock:", self.quantity)

    def update_stock(self, amount):

        self.quantity += amount

        print("Stock updated successfully!")

    def reduce_stock(self, amount):

        if amount <= self.quantity:

            self.quantity -= amount

            print("Stock reduced successfully!")

        else:

            print("Insufficient stock!")


# ------------------------------------------
# SUPPLIER CLASS
# ------------------------------------------

class Supplier:

    def __init__(self, supplier_id, name, phone):

        self.supplier_id = supplier_id
        self.name = name
        self.phone = phone

    def display_supplier(self):

        print("\nSupplier ID:", self.supplier_id)
        print("Supplier Name:", self.name)
        print("Phone:", self.phone)


# ------------------------------------------
# PURCHASE ORDER CLASS
# ------------------------------------------

class PurchaseOrder:

    def __init__(self, order_id, supplier, product, quantity):

        self.order_id = order_id
        self.supplier = supplier
        self.product = product
        self.quantity = quantity

        self.status = "Pending"

        self.created_date = datetime.now()

    def receive_order(self):

        self.product.update_stock(self.quantity)

        self.status = "Received"

        print("Purchase order received!")

    def display_order(self):

        print("\nPurchase Order:", self.order_id)

        print("Supplier:", self.supplier.name)

        print("Product:", self.product.name)

        print("Quantity:", self.quantity)

        print("Status:", self.status)


# ------------------------------------------
# INVENTORY MANAGEMENT
# ------------------------------------------

class Inventory:

    def __init__(self):

        self.products = {}

    def add_product(self, product):

        self.products[product.product_id] = product

        print("Product added successfully!")

    def show_inventory(self):

        print("\n========== INVENTORY ==========")

        for product in self.products.values():

            product.display_product()

    def check_stock(self, product_id):

        product = self.products.get(product_id)

        if product:

            print("Available:", product.quantity)

        else:

            print("Product not found!")

    def low_stock_alert(self):

        print("\n========== LOW STOCK ALERT ==========")

        for product in self.products.values():

            if product.quantity < 10:

                print(product.name, "has low stock!")

    def total_inventory_value(self):

        total = 0

        for product in self.products.values():

            total += product.price * product.quantity

        print("Total Inventory Value:", total)


# ------------------------------------------
# SALES MANAGEMENT
# ------------------------------------------

class Sales:

    def __init__(self):

        self.sales_history = []

    def sell_product(self, product, quantity):

        if quantity <= 0:

            print("Invalid quantity!")

            return

        if product.quantity >= quantity:

            product.reduce_stock(quantity)

            amount = product.price * quantity

            sale = {

                "product": product.name,

                "quantity": quantity,

                "amount": amount,

                "date": datetime.now()

            }

            self.sales_history.append(sale)

            print("Sale completed!")

            print("Total Amount:", amount)

        else:

            print("Insufficient stock!")

    def show_sales(self):

        print("\n========== SALES HISTORY ==========")

        for sale in self.sales_history:

            print(sale)

    def total_revenue(self):

        revenue = 0

        for sale in self.sales_history:

            revenue += sale["amount"]

        print("Total Revenue:", revenue)


# ------------------------------------------
# SUPPLY CHAIN APPLICATION
# ------------------------------------------

class SupplyChainSystem:

    def __init__(self):

        self.inventory = Inventory()

        self.sales = Sales()

        self.suppliers = {}

        self.purchase_orders = []

    def add_supplier(self, supplier):

        self.suppliers[supplier.supplier_id] = supplier

        print("Supplier registered!")

    def create_purchase_order(
        self, order_id, supplier_id, product_id, quantity
    ):

        supplier = self.suppliers.get(supplier_id)

        product = self.inventory.products.get(product_id)

        if supplier and product and quantity > 0:

            order = PurchaseOrder(
                order_id,
                supplier,
                product,
                quantity
            )

            self.purchase_orders.append(order)

            print("Purchase order created!")

        else:

            print("Invalid supplier, product or quantity!")

    def receive_purchase_order(self, order_id):

        for order in self.purchase_orders:

            if order.order_id == order_id:

                if order.status == "Pending":

                    order.receive_order()

                else:

                    print("Order already processed!")

                return

        print("Purchase order not found!")

    def show_purchase_orders(self):

        for order in self.purchase_orders:

            order.display_order()


# ------------------------------------------
# MAIN PROGRAM
# ------------------------------------------

def main():

    system = SupplyChainSystem()

    # Creating products

    p1 = Product(101, "Laptop", 50000, 25)

    p2 = Product(102, "Keyboard", 1000, 5)

    p3 = Product(103, "Mouse", 500, 15)

    system.inventory.add_product(p1)

    system.inventory.add_product(p2)

    system.inventory.add_product(p3)

    # Creating suppliers

    s1 = Supplier(1, "ABC Electronics", "9876543210")

    s2 = Supplier(2, "Global Traders", "9876543211")

    system.add_supplier(s1)

    system.add_supplier(s2)

    # Main menu

    while True:

        print("\n========== SUPPLY CHAIN SYSTEM ==========")

        print("1. Show Inventory")

        print("2. Add Product Stock")

        print("3. Sell Product")

        print("4. Low Stock Alert")

        print("5. Total Inventory Value")

        print("6. Create Purchase Order")

        print("7. Receive Purchase Order")

        print("8. Show Purchase Orders")

        print("9. Show Sales History")

        print("10. Total Revenue")

        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            system.inventory.show_inventory()

        elif choice == "2":

            product_id = int(input("Enter Product ID: "))

            quantity = int(input("Enter Quantity: "))

            product = system.inventory.products.get(product_id)

            if product and quantity > 0:

                product.update_stock(quantity)

            else:

                print("Invalid product or quantity!")

        elif choice == "3":

            product_id = int(input("Enter Product ID: "))

            quantity = int(input("Enter Quantity: "))

            product = system.inventory.products.get(product_id)

            if product:

                system.sales.sell_product(product, quantity)

            else:

                print("Product not found!")

        elif choice == "4":

            system.inventory.low_stock_alert()

        elif choice == "5":

            system.inventory.total_inventory_value()

        elif choice == "6":

            order_id = random.randint(1000, 9999)

            supplier_id = int(input("Supplier ID: "))

            product_id = int(input("Product ID: "))

            quantity = int(input("Quantity: "))

            system.create_purchase_order(
                order_id,
                supplier_id,
                product_id,
                quantity
            )

        elif choice == "7":

            order_id = int(input("Purchase Order ID: "))

            system.receive_purchase_order(order_id)

        elif choice == "8":

            system.show_purchase_orders()

        elif choice == "9":

            system.sales.show_sales()

        elif choice == "10":

            system.sales.total_revenue()

        elif choice == "0":

            print("Thank you for using the system!")

            break

        else:

            print("Invalid choice!")


if __name__ == "__main__":

    main()
