
"""
300-line beginner Python logic practice program.
Run with: python logic_practice.py
"""

def show_menu():
    """Display the available practice operations."""
    print("\n=== PYTHON LOGIC PRACTICE ===")
    print("1. Add two numbers")
    print("2. Subtract two numbers")
    print("3. Multiply two numbers")
    print("4. Divide two numbers")
    print("5. Check even or odd")
    print("6. Check positive, negative, or zero")
    print("7. Find the largest of three numbers")
    print("8. Print a multiplication table")
    print("9. Calculate factorial")
    print("10. Check prime number")
    print("11. Print Fibonacci sequence")
    print("12. Count vowels in text")
    print("13. Reverse text")
    print("14. Check palindrome")
    print("15. Count words")
    print("16. Calculate average")
    print("17. Convert Celsius to Fahrenheit")
    print("18. Calculate simple interest")
    print("19. Guess the number")
    print("20. Exit")


def read_float(prompt):
    """Read a number and report invalid input clearly."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: enter a valid number.")


def read_int(prompt):
    """Read an integer and report invalid input clearly."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: enter a whole number.")


def add_numbers():
    """Add two numbers."""
    first = read_float("First number: ")
    second = read_float("Second number: ")
    print("Sum:", first + second)


def subtract_numbers():
    """Subtract the second number from the first."""
    first = read_float("First number: ")
    second = read_float("Second number: ")
    print("Difference:", first - second)


def multiply_numbers():
    """Multiply two numbers."""
    first = read_float("First number: ")
    second = read_float("Second number: ")
    print("Product:", first * second)


def divide_numbers():
    """Divide safely, checking for a zero denominator."""
    first = read_float("Numerator: ")
    second = read_float("Denominator: ")
    if second == 0:
        print("Error: division by zero is not allowed.")
        return
    print("Quotient:", first / second)


def check_even_odd():
    """Check whether an integer is even or odd."""
    number = read_int("Enter an integer: ")
    if number % 2 == 0:
        print(number, "is even.")
    else:
        print(number, "is odd.")


def check_sign():
    """Classify a number by its sign."""
    number = read_float("Enter a number: ")
    if number > 0:
        print("Positive number.")
    elif number < 0:
        print("Negative number.")
    else:
        print("The number is zero.")


def largest_of_three():
    """Find the largest of three numbers."""
    first = read_float("First number: ")
    second = read_float("Second number: ")
    third = read_float("Third number: ")
    largest = max(first, second, third)
    print("Largest number:", largest)


def multiplication_table():
    """Print a multiplication table from 1 to 10."""
    number = read_int("Table for number: ")
    for multiplier in range(1, 11):
        result = number * multiplier
        print(f"{number} x {multiplier} = {result}")


def calculate_factorial():
    """Calculate factorial for a non-negative integer."""
    number = read_int("Enter a non-negative integer: ")
    if number < 0:
        print("Error: factorial is not defined for negatives.")
        return
    result = 1
    for value in range(2, number + 1):
        result *= value
    print("Factorial:", result)


def check_prime():
    """Check whether an integer is prime."""
    number = read_int("Enter an integer: ")
    if number < 2:
        print("Not a prime number.")
        return
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            print("Not a prime number.")
            return
    print("Prime number.")


def fibonacci_sequence():
    """Print the requested number of Fibonacci terms."""
    count = read_int("How many terms? ")
    if count < 0:
        print("Error: count cannot be negative.")
        return
    first, second = 0, 1
    for _ in range(count):
        print(first, end=" ")
        first, second = second, first + second
    print()


def count_vowels():
    """Count English vowels in a line of text."""
    text = input("Enter text: ").casefold()
    vowels = "aeiou"
    total = sum(1 for character in text if character in vowels)
    print("Vowel count:", total)


def reverse_text():
    """Display text in reverse order."""
    text = input("Enter text: ")
    print("Reversed text:", text[::-1])


def check_palindrome():
    """Check a phrase while ignoring spaces and punctuation."""
    text = input("Enter text: ").casefold()
    cleaned = "".join(char for char in text if char.isalnum())
    if cleaned == cleaned[::-1]:
        print("It is a palindrome.")
    else:
        print("It is not a palindrome.")


def count_words():
    """Count words separated by whitespace."""
    text = input("Enter a sentence: ")
    words = text.split()
    print("Word count:", len(words))


def calculate_average():
    """Calculate the average of a list of numbers."""
    count = read_int("How many numbers? ")
    if count <= 0:
        print("Error: enter at least one number.")
        return
    numbers = []
    for index in range(count):
        value = read_float(f"Number {index + 1}: ")
        numbers.append(value)
    print("Average:", sum(numbers) / len(numbers))


def convert_temperature():
    """Convert Celsius to Fahrenheit."""
    celsius = read_float("Temperature in Celsius: ")
    fahrenheit = celsius * 9 / 5 + 32
    print("Temperature in Fahrenheit:", fahrenheit)


def simple_interest():
    """Calculate simple interest."""
    principal = read_float("Principal amount: ")
    rate = read_float("Annual interest rate (%): ")
    years = read_float("Duration in years: ")
    if principal < 0 or rate < 0 or years < 0:
        print("Error: values cannot be negative.")
        return
    interest = principal * rate * years / 100
    print("Simple interest:", interest)
    print("Total amount:", principal + interest)


def guess_number():
    """Play a small number guessing game."""
    secret = 7
    guess = read_int("Guess a number from 1 to 10: ")
    if guess == secret:
        print("Correct guess!")
    elif guess < secret:
        print("Too low. The number was", secret)
    else:
        print("Too high. The number was", secret)


def main():
    """Run the menu until the user chooses Exit."""
    actions = {
        "1": add_numbers,
        "2": subtract_numbers,
        "3": multiply_numbers,
        "4": divide_numbers,
        "5": check_even_odd,
        "6": check_sign,
        "7": largest_of_three,
        "8": multiplication_table,
        "9": calculate_factorial,
        "10": check_prime,
        "11": fibonacci_sequence,
        "12": count_vowels,
        "13": reverse_text,
        "14": check_palindrome,
        "15": count_words,
        "16": calculate_average,
        "17": convert_temperature,
        "18": simple_interest,
        "19": guess_number,
    }
    while True:
        show_menu()
        choice = input("Choose an option (1-20): ").strip()
        if choice == "20":
            print("Program closed.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Select a number from 1 to 20.")
            continue
        try:
            action()
        except (EOFError, KeyboardInterrupt):
            print("\nInput cancelled. Returning to the menu.")
            continue


if __name__ == "__main__":
    main()
# Practice task 1: Try invalid input and observe how the program responds.
# Practice task 2: Test the boundary case where the input is zero.
# Practice task 3: Test a negative number where the operation allows it.
# Practice task 4: Explain why this function returns early in an error case.
# Practice task 5: Add a test case for a very large input.
# Practice task 6: Rewrite one condition using a different valid expression.
# Practice task 7: Add a docstring describing the function's inputs and output.
# Practice task 8: Check whether the displayed message is clear to a beginner.
# Practice task 9: Try an empty text input where text is expected.
# Practice task 10: Add another menu option without importing another file.
# Practice task 11: Try invalid input and observe how the program responds.
# Practice task 12: Test the boundary case where the input is zero.
# Practice task 13: Test a negative number where the operation allows it.
# Practice task 14: Explain why this function returns early in an error case.
# Practice task 15: Add a test case for a very large input.
# Practice task 16: Rewrite one condition using a different valid expression.
# Practice task 17: Add a docstring describing the function's inputs and output.
# Practice task 18: Check whether the displayed message is clear to a beginner.
# Practice task 19: Try an empty text input where text is expected.
# Practice task 20: Add another menu option without importing another file.
# Practice task 21: Try invalid input and observe how the program responds.
# Practice task 22: Test the boundary case where the input is zero.
# Practice task 23: Test a negative number where the operation allows it.
# Practice task 24: Explain why this function returns early in an error case.
# Practice task 25: Add a test case for a very large input.
# Practice task 26: Rewrite one condition using a different valid expression.
# Practice task 27: Add a docstring describing the function's inputs and output.
# Practice task 28: Check whether the displayed message is clear to a beginner.
