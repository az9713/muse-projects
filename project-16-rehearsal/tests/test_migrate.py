"""Migration tests: forward, rollback integrity, idempotence (8 tests)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from migrate import connect, down, dump_users, up, version


class MigrateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, "t.db")
        self.con = connect(self.db)

    def tearDown(self):
        self.con.close()
        self.tmp.cleanup()

    def seed(self):
        up(self.con, 1)
        self.con.executemany("INSERT INTO users (name) VALUES (?)", [("ann",), ("bo",)])
        self.con.commit()

    def test_forward_to_v3(self):
        self.seed()
        up(self.con, 3)
        self.assertEqual(version(self.con), 3)

    def test_backfill(self):
        self.seed()
        up(self.con, 2)
        emails = [row[0] for row in self.con.execute("SELECT email FROM users")]
        self.assertEqual(emails, ["ann@example.com", "bo@example.com"])

    def test_orders_table(self):
        self.seed()
        up(self.con, 3)
        tables = {row[0] for row in self.con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("orders", tables)

    def test_rollback_preserves_data(self):
        self.seed()
        before = dump_users(self.con)
        up(self.con, 3)
        down(self.con, 1)
        self.assertEqual(version(self.con), 1)
        self.assertEqual(dump_users(self.con), before)

    def test_idempotent_migrate(self):
        self.seed()
        up(self.con, 3)
        up(self.con, 3)
        self.assertEqual(version(self.con), 3)
        self.assertEqual(len(dump_users(self.con)), 2)

    def test_step_by_step(self):
        self.seed()
        for target in (2, 3):
            up(self.con, target)
            self.assertEqual(version(self.con), target)

    def test_full_rollback_to_zero(self):
        self.seed()
        up(self.con, 3)
        down(self.con, 0)
        self.assertEqual(version(self.con), 0)

    def test_rehearsal_log_exists_and_ok(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "REHEARSAL.log"), encoding="utf-8") as fh:
            lines = fh.read().strip().splitlines()
        self.assertTrue(lines[-1] == "REHEARSAL OK")
        self.assertTrue(any("byte-identical: True" in line for line in lines))


if __name__ == "__main__":
    unittest.main()
