"""Behavior tests for the typed app (10 tests)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.models import is_open, new_task
from app.service import complete, create, open_tasks


class TypedAppTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "t.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_assigns_ids(self):
        self.assertEqual(create("A", db_path=self.db).id, 1)
        self.assertEqual(create("B", db_path=self.db).id, 2)

    def test_create_normalizes_tags(self):
        task = create("A", ["B ", "a", "b"], self.db)
        self.assertEqual(task.tags, ["a", "b"])

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            create("   ", db_path=self.db)

    def test_new_task_strips(self):
        self.assertEqual(new_task(1, "  hi  ").title, "hi")

    def test_open_tasks(self):
        create("A", db_path=self.db)
        second = create("B", db_path=self.db)
        complete(second.id, self.db)
        self.assertEqual([t.title for t in open_tasks(self.db)], ["A"])

    def test_complete_missing(self):
        with self.assertRaises(KeyError):
            complete(99, self.db)

    def test_is_open(self):
        task = create("A", db_path=self.db)
        self.assertTrue(is_open(task))
        self.assertFalse(is_open(complete(task.id, self.db)))

    def test_persistence_round_trip(self):
        create("Keep", ["x"], self.db)
        [loaded] = open_tasks(self.db)
        self.assertEqual((loaded.title, loaded.tags), ("Keep", ["x"]))

    def test_tags_default_empty(self):
        self.assertEqual(create("A", db_path=self.db).tags, [])

    def test_done_defaults_false(self):
        self.assertFalse(create("A", db_path=self.db).done)


if __name__ == "__main__":
    unittest.main()
