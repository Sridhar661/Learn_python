"""Reusable input validation functions."""


def clean_name(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("This field must be text.")
    result = value.strip()
    if not result:
        raise ValueError("This field cannot be empty.")
    return result


def validate_non_negative(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be numeric.") from error
    if number < 0:
        raise ValueError(f"{label} cannot be negative.")
    return number


def validate_positive_int(value, label: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a whole number greater than zero.")
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{label} must be a whole number greater than zero."
        ) from error
    if number <= 0 or str(value).strip() != str(number):
        raise ValueError(f"{label} must be a whole number greater than zero.")
    return number
