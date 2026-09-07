"""Acceptance tests for the tags feature (plus pre-existing behaviors)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from tasks import service


class TagsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "t.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_with_tags(self):
        task = service.create_task("Write report", ["Work", "urgent"], self.db)
        self.assertEqual(task["tags"], ["urgent", "work"])

    def test_create_without_tags(self):
        task = service.create_task("Plain", [], self.db)
        self.assertEqual(task["tags"], [])

    def test_tags_deduped(self):
        task = service.create_task("Dup", ["a", "A ", "a"], self.db)
        self.assertEqual(task["tags"], ["a"])

    def test_empty_tag_rejected(self):
        with self.assertRaises(ValueError):
            service.create_task("Bad", ["ok", "  "], self.db)

    def test_filter_by_tag(self):
        service.create_task("One", ["work"], self.db)
        service.create_task("Two", ["home"], self.db)
        got = service.list_tasks(tag="work", db_path=self.db)
        self.assertEqual([t["title"] for t in got], ["One"])

    def test_filter_case_insensitive(self):
        service.create_task("One", ["Work"], self.db)
        self.assertEqual(len(service.list_tasks(tag="WORK", db_path=self.db)), 1)

    def test_filter_empty_tag_rejected(self):
        with self.assertRaises(ValueError):
            service.list_tasks(tag="  ", db_path=self.db)

    def test_open_with_tag(self):
        task = service.create_task("One", ["work"], self.db)
        service.create_task("Two", ["work"], self.db)
        service.complete_task(task["id"], self.db)
        self.assertEqual(len(service.open_tasks(tag="work", db_path=self.db)), 1)

    def test_empty_title_still_rejected(self):
        with self.assertRaises(ValueError):
            service.create_task("   ", ["work"], self.db)

    def test_done_flow_intact(self):
        task = service.create_task("One", [], self.db)
        done = service.complete_task(task["id"], self.db)
        self.assertTrue(done["done"])


if __name__ == "__main__":
    unittest.main()
