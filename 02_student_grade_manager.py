"""A simple student marks and grade management program."""
import json
from pathlib import Path

DATA_FILE = Path("students.json")
SUBJECTS = ["Python", "Mathematics", "Science"]


def load_students():
    """Read student records from a JSON file."""
    if not DATA_FILE.exists():
        return []
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("The data file is damaged; starting with an empty list.")
        return []


def save_students(students):
    """Write student records to disk."""
    DATA_FILE.write_text(json.dumps(students, indent=4), encoding="utf-8")


def calculate_average(marks):
    """Return the average mark for a student."""
    return sum(marks.values()) / len(marks)


def calculate_grade(average):
    """Convert an average mark into a letter grade."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def add_student(students):
    """Collect a student's name and subject marks."""
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if any(item["name"].lower() == name.lower() for item in students):
        print("That student already exists.")
        return
    marks = {}
    for subject in SUBJECTS:
        while True:
            try:
                mark = float(input(f"{subject} mark (0-100): "))
                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break
                print("Mark must be between 0 and 100.")
            except ValueError:
                print("Please enter a number.")
    students.append({"name": name, "marks": marks})
    save_students(students)
    print("Student record saved.")


def list_students(students):
    """Print every student with average and grade."""
    if not students:
        print("No student records found.")
        return
    print("\nNAME                 AVERAGE    GRADE")
    print("-" * 42)
    for student in students:
        average = calculate_average(student["marks"])
        grade = calculate_grade(average)
        print(f"{student['name']:<21}{average:>8.2f}    {grade}")


def find_student(students):
    """Search for one student by name."""
    search_name = input("Enter name to search: ").strip().lower()
    for student in students:
        if student["name"].lower() == search_name:
            print("Name:", student["name"])
            for subject, mark in student["marks"].items():
                print(f"{subject}: {mark:g}")
            average = calculate_average(student["marks"])
            print(f"Average: {average:.2f}")
            print("Grade:", calculate_grade(average))
            return
    print("Student not found.")


def show_top_student(students):
    """Show the student with the highest average."""
    if not students:
        print("No records available.")
        return
