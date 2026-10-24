"""Command-line interface for the Task Tracker."""

import argparse

from task_tracker.service import add_task, complete_task, delete_task, get_tasks


def build_parser() -> argparse.ArgumentParser:
    """Build and return the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="A simple task tracker that stores tasks in a JSON file."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add_parser = commands.add_parser("add", help="Add a task")
    add_parser.add_argument("title", help="Task title")

    commands.add_parser("list", help="List all tasks")

    done_parser = commands.add_parser("done", help="Mark a task as completed")
    done_parser.add_argument("id", type=int, help="Task ID")

    delete_parser = commands.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    return parser


def main() -> None:
    """Parse arguments and execute the requested action."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "add":
            task = add_task(args.title)
            print(f"Added task #{task.id}: {task.title}")
        elif args.command == "list":
            tasks = get_tasks()
            if not tasks:
                print('No tasks yet. Add one with: python main.py add "Your task"')
                return
            for task in tasks:
                status = "✓" if task.completed else " "
                print(f"[{status}] #{task.id}: {task.title}")
        elif args.command == "done":
            task = complete_task(args.id)
            print(f"Completed task #{task.id}: {task.title}")
        elif args.command == "delete":
            delete_task(args.id)
            print(f"Deleted task #{args.id}.")
    except (ValueError, LookupError) as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
