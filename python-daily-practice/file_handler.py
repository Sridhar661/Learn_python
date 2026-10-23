import json
from pathlib import Path
from typing import Any


def save_json(file_path: str, data: dict[str, Any]) -> None:
    """Save a dictionary to a JSON file."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(file_path: str) -> dict[str, Any]:
    """Load JSON data from a file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Expected a JSON object.")

    return data
