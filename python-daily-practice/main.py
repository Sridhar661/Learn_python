from datetime import datetime
from algorithms import is_prime, fibonacci
from data_structures import remove_duplicates
from statistics_tools import calculate_average


def main():
    print("=" * 45)
    print("       PYTHON DAILY CODING PRACTICE")
    print("=" * 45)
    print("Date:", datetime.now().strftime("%Y-%m-%d"))

    numbers = [10, 20, 30, 20, 40, 10, 50]
    print("\nOriginal numbers:", numbers)
    print("Unique numbers:", remove_duplicates(numbers))
    print("Average:", calculate_average(numbers))
    print("First 10 Fibonacci numbers:", fibonacci(10))

    number = 29
    print(f"Is {number} prime? {is_prime(number)}")


if __name__ == "__main__":
    main()
