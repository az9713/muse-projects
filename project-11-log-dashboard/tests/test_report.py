"""Report tests: db + html agree with an independent parse (8 tests)."""
import os
import re
import sqlite3
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def independent():
    rows = []
    with open(os.path.join(ROOT, "logs", "access.log"), encoding="utf-8") as fh:
        for line in fh:
            _ip, _ts, _method, path, status, latency = line.split()
            rows.append((path, int(status), int(latency)))
    return rows


class ReportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = independent()
        cls.con = sqlite3.connect(os.path.join(ROOT, "report.db"))
        with open(os.path.join(ROOT, "report.html"), encoding="utf-8") as fh:
            cls.html = fh.read()

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_row_count(self):
        n = self.con.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
        self.assertEqual(n, 2000)
        self.assertEqual(n, len(self.rows))

    def test_error_count_matches(self):
        expected = sum(1 for _, status, _ in self.rows if status >= 500)
        n = self.con.execute("SELECT COUNT(*) FROM requests WHERE status >= 500").fetchone()[0]
        self.assertEqual(n, expected)
        self.assertGreater(n, 0)

    def test_statuses_only_200_500(self):
        codes = {r[0] for r in self.con.execute("SELECT DISTINCT status FROM requests")}
        self.assertEqual(codes, {200, 500})

    def test_slowest_path_is_search(self):
        top = self.con.execute(
            "SELECT path FROM requests GROUP BY path ORDER BY AVG(latency_ms) DESC"
        ).fetchone()[0]
        self.assertEqual(top, "/search")

    def test_busiest_path_is_health(self):
        top = self.con.execute(
            "SELECT path FROM requests GROUP BY path ORDER BY COUNT(*) DESC"
        ).fetchone()[0]
        self.assertEqual(top, "/health")

    def test_p95_matches_independent(self):
        ordered = sorted(lat for _, _, lat in self.rows)
        expected = ordered[min(len(ordered) - 1, int(len(ordered) * 95 / 100))]
        m = re.search(r"p95=(\d+)ms", self.html)
        self.assertIsNotNone(m)
        self.assertEqual(int(m.group(1)), expected)

    def test_html_lists_all_paths(self):
        for path in {p for p, _, _ in self.rows}:
            self.assertIn(path, self.html)

    def test_html_totals_match(self):
        m = re.search(r"requests=(\d+) errors=(\d+)", self.html)
        self.assertIsNotNone(m)
        self.assertEqual(int(m.group(1)), 2000)
        expected = sum(1 for _, status, _ in self.rows if status >= 500)
        self.assertEqual(int(m.group(2)), expected)


if __name__ == "__main__":
    unittest.main()
