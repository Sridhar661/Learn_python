"""Functions can have default parameter values."""

def describe_pet(name, animal="dog"):
    print(f"{name} is a {animal}.")


describe_pet("Bruno")
describe_pet("Milo", "cat")
