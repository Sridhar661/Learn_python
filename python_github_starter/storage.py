"""JSON persistence for task data."""

import json
from pathlib import Path


class JsonTaskStorage:
    def __init__(self, path: str | Path = "data/tasks.json"):
        self.path = Path(path)

    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"Task data file contains invalid JSON: {self.path}") from error

        if not isinstance(data, list):
            raise ValueError("Task data must be a JSON list.")
        return data

    def save(self, tasks: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(tasks, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary_path.replace(self.path)
