# ============================================================
# STUDENT MANAGEMENT SYSTEM
# Features: Add, View, Search, Update, Delete, and Grade Reports
# ============================================================

from datetime import datetime

students = {}
next_student_id = 1001


def display_header(title):
    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def calculate_average(marks):
    if not marks:
        return 0

    return sum(marks.values()) / len(marks)


def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def add_student():
    global next_student_id

    display_header("ADD NEW STUDENT")

    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    age_text = input("Enter student age: ").strip()

    try:
        age = int(age_text)
        if age < 5 or age > 100:
            print("Enter an age between 5 and 100.")
            return
    except ValueError:
        print("Invalid age.")
        return

    department = input("Enter department: ").strip()

    if not department:
        print("Department cannot be empty.")
        return

    students[next_student_id] = {
        "name": name,
        "age": age,
        "department": department,
        "marks": {},
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
    }

    print(f"Student added successfully!")
    print(f"Student ID: {next_student_id}")

    next_student_id += 1


def view_all_students():
    display_header("ALL STUDENTS")

    if not students:
        print("No students registered.")
        return

    print(
        f"{'ID':<10}{'Name':<20}"
        f"{'Age':<8}{'Department':<20}"
    )
    print("-" * 60)

    for student_id, student in students.items():
        print(
            f"{student_id:<10}"
            f"{student['name']:<20}"
            f"{student['age']:<8}"
            f"{student['department']:<20}"
        )


def search_student():
    display_header("SEARCH STUDENT")

    keyword = input(
        "Enter student ID or name: "
    ).strip().lower()

    found = False

    for student_id, student in students.items():
        if (
            keyword == str(student_id)
            or keyword in student["name"].lower()
        ):
            average = calculate_average(student["marks"].values())
            grade = calculate_grade(average)

            print(f"\nStudent ID: {student_id}")
            print(f"Name: {student['name']}")
            print(f"Age: {student['age']}")
            print(f"Department: {student['department']}")
            print(f"Average: {average:.2f}")
            print(f"Grade: {grade}")

            found = True

    if not found:
        print("Student not found.")


def update_student():
    display_header("UPDATE STUDENT DETAILS")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    print("1. Update name")
    print("2. Update age")
    print("3. Update department")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Enter new name: ").strip()

        if name:
            student["name"] = name
            print("Name updated successfully.")

    elif choice == "2":
        try:
            age = int(input("Enter new age: "))

            if 5 <= age <= 100:
                student["age"] = age
                print("Age updated successfully.")
            else:
                print("Age must be between 5 and 100.")

        except ValueError:
            print("Invalid age.")

    elif choice == "3":
        department = input("Enter new department: ").strip()

        if department:
            student["department"] = department
            print("Department updated successfully.")

    else:
        print("Invalid choice.")


def delete_student():
    display_header("DELETE STUDENT")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]

    confirmation = input(
        f"Delete {student['name']}? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        del students[student_id]
        print("Student deleted successfully.")
    else:
        print("Deletion cancelled.")


def enter_marks():
    display_header("ENTER STUDENT MARKS")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    if student_id not in students:
        print("Student not found.")
        return

    subjects = ["Tamil", "English", "Maths", "Science", "Social"]

    student = students[student_id]

    for subject in subjects:
        while True:
            try:
                mark = float(
                    input(f"Enter marks for {subject} (0-100): ")
                )

                if 0 <= mark <= 100:
                    student["marks"][subject] = mark
                    break

                print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    print("Marks saved successfully.")


def generate_report():
    display_header("STUDENT MARKS REPORT")

    try:
        student_id = int(input("Enter student ID: "))
    except ValueError:
        print("Invalid student ID.")
        return

    if student_id not in students:
        print("Student not found.")
        return

    student = students[student_id]
    marks = student["marks"]

    if not marks:
        print("Marks have not been entered.")
        return

    print(f"Student: {student['name']}")
    print(f"Student ID: {student_id}")
    print("-" * 40)

    for subject, mark in marks.items():
        print(f"{subject:<20}: {mark:.2f}")

    average = calculate_average(marks.values())
    total = sum(marks.values())
    grade = calculate_grade(average)

    print("-" * 40)
    print(f"Total Marks: {total:.2f}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {grade}")

    if all(mark >= 35 for mark in marks.values()):
        print("Result: PASS")
    else:
        print("Result: FAIL")


def show_topper():
    display_header("TOP STUDENT REPORT")

    students_with_marks = [
        (student_id, student)
        for student_id, student in students.items()
        if student["marks"]
    ]

    if not students_with_marks:
        print("No student marks available.")
        return

    topper_id, topper = max(
        students_with_marks,
        key=lambda item: calculate_average(
            item[1]["marks"].values()
        ),
    )

    average = calculate_average(topper["marks"].values())

    print(f"Topper ID: {topper_id}")
    print(f"Name: {topper['name']}")
    print(f"Average: {average:.2f}")
    print(f"Grade: {calculate_grade(average)}")


def main():
    while True:
        display_header("STUDENT MANAGEMENT SYSTEM")

        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Enter Marks")
        print("7. Generate Marks Report")
        print("8. Show Topper")
        print("9. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            enter_marks()
        elif choice == "7":
            generate_report()
        elif choice == "8":
            show_topper()
        elif choice == "9":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Select 1-9.")


if __name__ == "__main__":
    main()