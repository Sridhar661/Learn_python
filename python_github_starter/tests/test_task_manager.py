import tempfile
import unittest
from pathlib import Path

from storage import JsonTaskStorage
from task_manager import TaskManager


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        storage = JsonTaskStorage(Path(self.temp_dir.name) / "tasks.json")
        self.manager = TaskManager(storage)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_list_task(self):
        task = self.manager.add_task("Learn Python")
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Learn Python")
        self.assertFalse(task["completed"])
        self.assertEqual(len(self.manager.list_tasks()), 1)

    def test_reject_empty_title(self):
        with self.assertRaises(ValueError):
            self.manager.add_task("   ")

    def test_complete_task(self):
        task = self.manager.add_task("Write tests")
        completed = self.manager.complete_task(task["id"])
        self.assertTrue(completed["completed"])

    def test_delete_task(self):
        task = self.manager.add_task("Temporary task")
        self.manager.delete_task(task["id"])
        self.assertEqual(self.manager.list_tasks(), [])

    def test_unknown_task_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.manager.complete_task(999)


if __name__ == "__main__":
    unittest.main()
