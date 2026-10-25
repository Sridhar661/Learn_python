"""Lists store ordered, changeable collections."""

fruits = ["apple", "banana", "mango"]
print("First fruit:", fruits[0])

fruits.append("orange")
fruits[1] = "grapes"
print("All fruits:", fruits)
print("Number of fruits:", len(fruits))

for fruit in fruits:
    print(fruit)
