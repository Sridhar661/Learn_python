"""Business logic for creating and managing tasks."""

from storage import JsonTaskStorage
from utils import validate_title


class TaskManager:
    def __init__(self, storage=None):
        self.storage = storage or JsonTaskStorage()
        self.tasks = self.storage.load()

    def _save(self) -> None:
        self.storage.save(self.tasks)

    def add_task(self, title: str) -> dict:
        clean_title = validate_title(title)
        next_id = max((task["id"] for task in self.tasks), default=0) + 1
        task = {"id": next_id, "title": clean_title, "completed": False}
        self.tasks.append(task)
        self._save()
        return task.copy()

    def list_tasks(self) -> list[dict]:
        return [task.copy() for task in self.tasks]

    def complete_task(self, task_id: int) -> dict:
        task = self._find_task(task_id)
        task["completed"] = True
        self._save()
        return task.copy()

    def delete_task(self, task_id: int) -> None:
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self._save()

    def _find_task(self, task_id: int) -> dict:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise KeyError(f"No task found with ID {task_id}")
