```python
class Student:
    def __init__(self, student_id, name, age, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = marks

    def calculate_grade(self):
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 50:
            return "D"
        else:
            return "Fail"

    def display(self):
        print("-" * 35)
        print(f"Student ID : {self.student_id}")
        print(f"Name       : {self.name}")
        print(f"Age        : {self.age}")
        print(f"Marks      : {self.marks}")
        print(f"Grade      : {self.calculate_grade()}")
        print("-" * 35)


class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        if self.find_student(student.student_id):
            print("Student ID already exists.")
            return False

        self.students.append(student)
        print("Student added successfully.")
        return True

    def find_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def display_all(self):
        if not self.students:
            print("No students available.")
            return

        for student in self.students:
            student.display()

    def search_student(self, student_id):
        student = self.find_student(student_id)

        if student:
            student.display()
        else:
            print("Student not found.")

    def update_marks(self, student_id, new_marks):
        student = self.find_student(student_id)

        if student:
            student.marks = new_marks
            print("Marks updated successfully.")
        else:
            print("Student not found.")

    def delete_student(self, student_id):
        student = self.find_student(student_id)

        if student:
            self.students.remove(student)
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def calculate_average(self):
        if not self.students:
            print("No students available.")
            return

        total = sum(student.marks for student in self.students)
        average = total / len(self.students)
        print(f"Class average: {average:.2f}")

    def show_topper(self):
        if not self.students:
            print("No students available.")
            return

        topper = max(self.students, key=lambda s: s.marks)
        print("Class Topper:")
        topper.display()


```python
from student import Student, StudentManager


def get_integer(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid integer.")


def get_marks():
    while True:
        try:
            marks = float(input("Enter marks (0-100): "))
            if 0 <= marks <= 100:
                return marks
            print("Marks must be between 0 and 100.")
        except ValueError:
            print("Please enter a valid number.")


def add_student(manager):
    student_id = get_integer("Enter student ID: ")

    if manager.find_student(student_id):
        print("Student ID already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    age = get_integer("Enter student age: ")

    if age <= 0:
        print("Age must be greater than zero.")
        return

    marks = get_marks()

    student = Student(student_id, name, age, marks)
    manager.add_student(student)


def main():
    manager = StudentManager()

    # Sample students
    manager.add_student(Student(1, "Arun", 20, 85))
    manager.add_student(Student(2, "Priya", 21, 92))
    manager.add_student(Student(3, "Kumar", 19, 67))

    while True:
        print("\n===== STUDENT MANAGEMENT =====")
        print("1. Add Student")
        print("2. Display All Students")
        print("3. Search Student")
        print("4. Update Marks")
        print("5. Delete Student")
        print("6. Calculate Class Average")
        print("7. Show Topper")
        print("8. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(manager)

        elif choice == "2":
            manager.display_all()

        elif choice == "3":
            student_id = get_integer("Enter student ID: ")
            manager.search_student(student_id)

        elif choice == "4":
            student_id = get_integer("Enter student ID: ")
            marks = get_marks()
            manager.update_marks(student_id, marks)

        elif choice == "5":
            student_id = get_integer("Enter student ID: ")
            manager.delete_student(student_id)

        elif choice == "6":
            manager.calculate_average()

        elif choice == "7":
            manager.show_topper()

        elif choice == "8":
            print("Thank you for using the application.")
            break

        else:
            print("Invalid option. Choose 1 to 8.")


if __name__ == "__main__":
    main()
```

