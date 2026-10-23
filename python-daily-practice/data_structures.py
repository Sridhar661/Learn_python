from collections import Counter, deque
from typing import TypeVar

T = TypeVar("T")


def remove_duplicates(items: list[T]) -> list[T]:
    """Remove duplicates while preserving order."""
    return list(dict.fromkeys(items))


def count_frequency(items: list[T]) -> dict[T, int]:
    """Count how often each item appears."""
    return dict(Counter(items))


class TaskQueue:
    """A simple first-in, first-out task queue."""

    def __init__(self):
        self._tasks = deque()

    def add_task(self, task: str) -> None:
        self._tasks.append(task)

    def process_task(self) -> str | None:
        if not self._tasks:
            return None
        return self._tasks.popleft()

    def pending_tasks(self) -> int:
        return len(self._tasks)
