"""Dictionaries store key-value pairs."""

student = {
    "name": "Kavi",
    "age": 21,
    "course": "Computer Science",
}

print("Name:", student["name"])
student["age"] = 22
student["city"] = "Chennai"

for key, value in student.items():
    print(f"{key}: {value}")
