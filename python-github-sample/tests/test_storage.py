"""Unit tests for task storage."""

import json
import tempfile
import unittest
from pathlib import Path

from task_tracker.models import Task
from task_tracker.storage import load_tasks, save_tasks


class StorageTests(unittest.TestCase):
    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tasks.json"
            self.assertEqual(load_tasks(path), [])

    def test_save_and_load_tasks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "nested" / "tasks.json"
            expected = [
                Task(id=1, title="Learn Python"),
                Task(id=2, title="Push to GitHub", completed=True),
            ]
            save_tasks(expected, path)
            self.assertEqual(load_tasks(path), expected)

    def test_invalid_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tasks.json"
            path.write_text("{invalid json", encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tasks(path)

    def test_non_list_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "tasks.json"
            path.write_text(json.dumps({"id": 1}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_tasks(path)


if __name__ == "__main__":
    unittest.main()
