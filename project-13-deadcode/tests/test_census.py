"""Census tests: finds planted dead, proves src/ clean (8 tests)."""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from census import census
from src.app import count_admins, greet
from src.models import User


class CensusTest(unittest.TestCase):
    def test_finds_three_fixture_dead(self):
        dead = census(os.path.join(ROOT, "fixtures"))
        self.assertEqual(len(dead), 3)

    def test_names_reported(self):
        dead = " ".join(census(os.path.join(ROOT, "fixtures")))
        self.assertIn("orphan_function", dead)
        self.assertIn("OrphanClass", dead)
        self.assertIn("live_entry", dead)
        self.assertNotIn("used_fn", dead)

    def test_src_is_clean(self):
        self.assertEqual(census(os.path.join(ROOT, "src")), [])

    def test_greet(self):
        self.assertEqual(greet("ann"), "HELLO, ANN")

    def test_count_admins(self):
        users = [User("a", True), User("b"), User("c", True)]
        self.assertEqual(count_admins(users), 2)

    def test_user_defaults(self):
        self.assertFalse(User("x").admin)

    def test_no_dead_mod_file(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "src", "dead_mod.py")))

    def test_no_orphan_symbols_in_src(self):
        joined = " ".join(census(os.path.join(ROOT, "src")))
        self.assertNotIn("orphan", joined.lower())


if __name__ == "__main__":
    unittest.main()
