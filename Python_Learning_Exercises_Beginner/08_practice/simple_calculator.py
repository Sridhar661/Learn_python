"""A simple calculator for two numbers."""

first = float(input("Enter the first number: "))
operator = input("Choose +, -, *, or /: ").strip()
second = float(input("Enter the second number: "))

if operator == "+":
    result = first + second
elif operator == "-":
    result = first - second
elif operator == "*":
    result = first * second
elif operator == "/":
    if second == 0:
        result = None
        print("Cannot divide by zero.")
    else:
        result = first / second
else:
    result = None
    print("Unknown operator.")

if result is not None:
    print("Result:", result)
