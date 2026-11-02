
# ==========================================
# STUDENT MANAGEMENT SYSTEM
# ==========================================

students = []


def add_student():
    print("\n--- Add Student ---")

    student_id = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    age = int(input("Enter Age: "))
    department = input("Enter Department: ")
    marks = float(input("Enter Marks: "))

    student = {
        "id": student_id,
        "name": name,
        "age": age,
        "department": department,
        "marks": marks
    }

    students.append(student)
    print("Student added successfully!")


def view_students():
    print("\n--- Student List ---")

    if not students:
        print("No students available.")
        return

    for student in students:
        print("-" * 40)
        print("ID:", student["id"])
        print("Name:", student["name"])
        print("Age:", student["age"])
        print("Department:", student["department"])
        print("Marks:", student["marks"])


def search_student():
    student_id = input("Enter Student ID to search: ")

    for student in students:
        if student["id"] == student_id:
            print("\nStudent Found!")
            print(student)
            return

    print("Student not found.")


def update_student():
    student_id = input("Enter Student ID: ")

    for student in students:
        if student["id"] == student_id:

            print("1. Update Name")
            print("2. Update Age")
            print("3. Update Department")
            print("4. Update Marks")

            choice = input("Select option: ")

            if choice == "1":
                student["name"] = input("New Name: ")

            elif choice == "2":
                student["age"] = int(input("New Age: "))

            elif choice == "3":
                student["department"] = input("New Department: ")

            elif choice == "4":
                student["marks"] = float(input("New Marks: "))

            else:
                print("Invalid option!")
                return

            print("Student updated successfully!")
            return

    print("Student not found.")


def delete_student():
    student_id = input("Enter Student ID: ")

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            print("Student deleted successfully!")
            return

    print("Student not found.")


def calculate_average():
    if not students:
        print("No student records.")
        return

    total = sum(student["marks"] for student in students)
    average = total / len(students)

    print("Average Marks:", round(average, 2))


def show_topper():
    if not students:
        print("No student records.")
        return

    topper = max(students, key=lambda x: x["marks"])

    print("\nClass Topper:")
    print("Name:", topper["name"])
    print("Marks:", topper["marks"])


def show_passed_students():
    print("\nPassed Students:")

    for student in students:
        if student["marks"] >= 35:
            print(student["name"], student["marks"])


def show_failed_students():
    print("\nFailed Students:")

    for student in students:
        if student["marks"] < 35:
            print(student["name"], student["marks"])


def sort_students():
    students.sort(key=lambda x: x["marks"], reverse=True)

    print("\nStudents sorted by marks:")
    view_students()


def show_statistics():
    if not students:
        print("No records available.")
        return

    print("\n--- Statistics ---")
    print("Total Students:", len(students))
    print("Average Marks:", sum(s["marks"] for s in students) / len(students))
    print("Highest Marks:", max(s["marks"] for s in students))
    print("Lowest Marks:", min(s["marks"] for s in students))


def menu():
    while True:
        print("\n========== STUDENT MANAGEMENT ==========")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Calculate Average")
        print("7. Show Topper")
        print("8. Passed Students")
        print("9. Failed Students")
        print("10. Sort Students")
        print("11. Show Statistics")
        print("12. Exit")

        choice = input("\nEnter your choice: ")

        try:
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
                show_topper()
            elif choice == "8":
                show_passed_students()
            elif choice == "9":
                show_failed_students()
            elif choice == "10":
                sort_students()
            elif choice == "11":
                show_statistics()
            elif choice == "12":
                print("Thank you!")
                break
            else:
                print("Invalid choice!")

        except ValueError:
            print("Please enter valid numerical values.")


if __name__ == "__main__":
    menu()
