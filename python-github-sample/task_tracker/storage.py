"""JSON storage functions for tasks."""

import json
from pathlib import Path

from task_tracker.models import Task

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def load_tasks(file_path: Path = DEFAULT_DATA_FILE) -> list[Task]:
    """Load tasks from JSON; return an empty list if the file does not exist."""
    if not file_path.exists():
        return []

    try:
        raw_data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Task data is not valid JSON: {file_path}") from exc

    if not isinstance(raw_data, list):
        raise ValueError("Task data must be a JSON list.")

    return [Task.from_dict(item) for item in raw_data]


def save_tasks(tasks: list[Task], file_path: Path = DEFAULT_DATA_FILE) -> None:
    """Save tasks to JSON, creating the parent folder if necessary."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    content = [task.to_dict() for task in tasks]
    file_path.write_text(
        json.dumps(content, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
