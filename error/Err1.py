try:
    a = 10
    b = 0
    print(a / b)
except ZeroDivisionError:
    print("Error: Cannot divide by zero")















try:
    number = int(input("Enter a number: "))
    print("Number:", number)
except ValueError:
    print("Error: Please enter a valid integer")    