"""Handle common input errors gracefully."""

try:
    number = int(input("Enter a whole number: "))
    print("Double:", number * 2)
except ValueError:
    print("That was not a valid whole number. Please try again.")
