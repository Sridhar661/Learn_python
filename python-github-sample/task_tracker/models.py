"""Data model for tasks."""

from dataclasses import asdict, dataclass


@dataclass
class Task:
    """Represent one task."""

    id: int
    title: str
    completed: bool = False

    def to_dict(self) -> dict:
        """Convert the task into a JSON-compatible dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """Create a task from a dictionary."""
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            completed=bool(data.get("completed", False)),
        )
