"""Command-line interface for the task tracker."""

from task_manager import TaskManager


def show_menu() -> None:
    print("\n=== Python Task Tracker ===")
    print("1. Add task")
    print("2. List tasks")
    print("3. Mark task complete")
    print("4. Delete task")
    print("5. Exit")


def main() -> None:
    manager = TaskManager()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            try:
                task = manager.add_task(title)
                print(f"Added task #{task['id']}: {task['title']}")
            except ValueError as error:
                print(f"Error: {error}")
        elif choice == "2":
            tasks = manager.list_tasks()
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                status = "✓" if task["completed"] else " "
                print(f"[{status}] #{task['id']} - {task['title']}")
        elif choice == "3":
            try:
                task_id = int(input("Task ID to complete: "))
                task = manager.complete_task(task_id)
                print(f"Completed: {task['title']}")
            except (ValueError, KeyError) as error:
                print(f"Could not complete task: {error}")
        elif choice == "4":
            try:
                task_id = int(input("Task ID to delete: "))
                manager.delete_task(task_id)
                print(f"Deleted task #{task_id}.")
            except (ValueError, KeyError) as error:
                print(f"Could not delete task: {error}")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
