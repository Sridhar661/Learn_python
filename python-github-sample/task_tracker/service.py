"""Business logic for managing tasks."""

from task_tracker.models import Task
from task_tracker.storage import load_tasks, save_tasks


def add_task(title: str) -> Task:
    """Create and save a new task."""
    cleaned_title = title.strip()
    if not cleaned_title:
        raise ValueError("Task title cannot be empty.")

    tasks = load_tasks()
    next_id = max((task.id for task in tasks), default=0) + 1
    task = Task(id=next_id, title=cleaned_title)
    tasks.append(task)
    save_tasks(tasks)
    return task


def get_tasks() -> list[Task]:
    """Return all saved tasks, ordered by ID."""
    return sorted(load_tasks(), key=lambda task: task.id)


def complete_task(task_id: int) -> Task:
    """Mark a task as completed and save the change."""
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            save_tasks(tasks)
            return task
    raise LookupError(f"No task found with ID {task_id}.")


def delete_task(task_id: int) -> None:
    """Delete a task by ID."""
    tasks = load_tasks()
    remaining = [task for task in tasks if task.id != task_id]
    if len(remaining) == len(tasks):
        raise LookupError(f"No task found with ID {task_id}.")
    save_tasks(remaining)
