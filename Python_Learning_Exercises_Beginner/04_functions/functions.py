"""Create reusable blocks of code with functions."""

def greet(name):
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


print(greet("Priya"))
print("4 + 6 =", add(4, 6))
