def is_prime(number: int) -> bool:
    """Return True if a number is prime."""
    if number < 2:
        return False

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1

    return True


def fibonacci(count: int) -> list[int]:
    """Generate the first count Fibonacci numbers."""
    if count < 0:
        raise ValueError("Count cannot be negative.")

    sequence = []
    first, second = 0, 1

    for _ in range(count):
        sequence.append(first)
        first, second = second, first + second

    return sequence


def binary_search(numbers: list[int], target: int) -> int:
    """Find a target in a sorted list; return its index or -1."""
    left, right = 0, len(numbers) - 1

    while left <= right:
        middle = (left + right) // 2

        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1

    return -1
