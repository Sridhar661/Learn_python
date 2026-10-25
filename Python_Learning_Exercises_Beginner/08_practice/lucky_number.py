"""Return True if a list contains a number divisible by 7."""

def has_lucky_number(numbers):
    for number in numbers:
        if number % 7 == 0:
            return True
    return False


print(has_lucky_number([1, 3, 8]))       # False
print(has_lucky_number([2, 14, 20]))     # True
