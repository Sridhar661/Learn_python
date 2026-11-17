
# Student Management System
# 1
students = {}

def add_student():
    student_id = input("Enter student ID: ")
    if student_id in students:
        print("Student already exists!")
        return
    name = input("Enter student name: ")
    age = int(input("Enter student age: "))
    marks = float(input("Enter student marks: "))
    students[student_id] = {
        "name": name,
        "age": age,
        "marks": marks
    }
    print("Student added successfully!")

def view_students():
    if not students:
        print("No students found!")
        return
    for sid, details in students.items():
        print("\nStudent ID:", sid)
        print("Name:", details["name"])
        print("Age:", details["age"])
        print("Marks:", details["marks"])

def search_student():
    sid = input("Enter student ID: ")
    if sid in students:
        print("Student details:", students[sid])
    else:
        print("Student not found!")

def update_student():
    sid = input("Enter student ID: ")
    if sid not in students:
        print("Student not found!")
        return
    name = input("Enter new name: ")
    age = int(input("Enter new age: "))
    marks = float(input("Enter new marks: "))
    students[sid]["name"] = name
    students[sid]["age"] = age
    students[sid]["marks"] = marks
    print("Student updated!")

def delete_student():
    sid = input("Enter student ID: ")
    if sid in students:
        del students[sid]
        print("Student deleted!")
    else:
        print("Student not found!")

def calculate_average():
    if not students:
        print("No records available!")
        return
    total = sum(s["marks"] for s in students.values())
    average = total / len(students)
    print("Class average:", round(average, 2))

def find_topper():
    if not students:
        print("No records available!")
        return
    topper_id = max(students, key=lambda x: students[x]["marks"])
    print("Class topper:", students[topper_id]["name"])
    print("Top marks:", students[topper_id]["marks"])

def show_menu():
    print("\n===== STUDENT MANAGEMENT =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Calculate Average")
    print("7. Find Topper")
    print("8. Exit")

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            calculate_average()
        elif choice == "7":
            find_topper()
        elif choice == "8":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
