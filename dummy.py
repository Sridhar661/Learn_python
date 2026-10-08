balance = 10000
pin = 1234

entered_pin = int(input("Enter your PIN: "))

if entered_pin == pin:
    print("\n1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("Your balance is ₹", balance)

    elif choice == 2:
        amount = float(input("Enter deposit amount: ₹"))
        balance += amount
        print("Deposited successfully!")
        print("New balance: ₹", balance)

    elif choice == 3:
        amount = float(input("Enter withdrawal amount: ₹"))

        if amount <= balance:
            balance -= amount
            print("Please collect your cash.")
            print("Remaining balance: ₹", balance)
        else:
            print("Insufficient balance!")

    elif choice == 4:
        print("Thank you!")

    else:
        print("Invalid choice!")

else:
    print("Incorrect PIN!")












