"""Read and write inventory information in JSON format."""

import json
from pathlib import Path


class JsonStorage:
    def __init__(self, path: str | Path = "data/inventory.json"):
        self.path = Path(path)

    def load(self) -> dict:
        if not self.path.exists():
            return {"products": [], "sales": []}

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Cannot parse inventory file: {self.path}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError("Inventory data must be a JSON object.")
        data.setdefault("products", [])
        data.setdefault("sales", [])
        return data

    def save(self, data: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(self.path)
