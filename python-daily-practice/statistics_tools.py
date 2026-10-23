def calculate_average(numbers: list[float]) -> float:
    """Calculate the arithmetic mean."""
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list.")

    return sum(numbers) / len(numbers)


def find_min_max(numbers: list[float]) -> tuple[float, float]:
    """Return the minimum and maximum values."""
    if not numbers:
        raise ValueError("The list cannot be empty.")

    return min(numbers), max(numbers)


def calculate_median(numbers: list[float]) -> float:
    """Calculate the median without modifying the original list."""
    if not numbers:
        raise ValueError("Cannot calculate median of an empty list.")

    ordered = sorted(numbers)
    middle = len(ordered) // 2

    if len(ordered) % 2:
        return ordered[middle]

    return (ordered[middle - 1] + ordered[middle]) / 2
