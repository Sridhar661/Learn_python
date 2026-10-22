# Simple Python Student Management Program
students = []

def add_student(name, age, marks):
    student = {
        "name": name,
        "age": age,
        "marks": marks
    }
    students.append(student)
    print(f"{name} added successfully.")

def display_students():
    if not students:
        print("No students found.")
        return
    for student in students:
        print(student)

def calculate_average():
    if not students:
        return 0
    total = sum(s["marks"] for s in students)
    return total / len(students)

def find_student(name):
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None

def show_topper():
    if not students:
        print("No students available.")
        return
    topper = max(students, key=lambda s: s["marks"])
    print("Topper:", topper["name"])

add_student("Arun", 21, 85)
add_student("Priya", 22, 92)
add_student("Kumar", 20, 78)

display_students()
print("Average marks:", calculate_average())
show_topper()

result = find_student("Priya")
if result:
    print("Student found:", result)
else:
    print("Student not found.")

for student in students:
    if student["marks"] >= 90:
        print(student["name"], "Grade A")
    elif student["marks"] >= 80:
        print(student["name"], "Grade B")
    elif student["marks"] >= 70:
        print(student["name"], "Grade C")
    else:
        print(student["name"], "Needs improvement")

print("Total students:", len(students))
print("Program completed successfully.")