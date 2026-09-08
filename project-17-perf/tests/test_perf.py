"""Perf tests: bench output, gate pass/fail, trend page (8 tests)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)


def run(*args):
    return subprocess.run([sys.executable, *args], capture_output=True, text=True, check=False, cwd=ROOT)


class PerfTest(unittest.TestCase):
    def test_bench_appends_valid_jsonl(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = os.path.join(tmp, "r.jsonl")
            proc = run("bench.py", "--runs", runs, "--repeat", "1")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(runs, encoding="utf-8") as fh:
                rows = [json.loads(line) for line in fh]
            self.assertEqual(len(rows), 3)
            self.assertEqual({r["bench"] for r in rows}, {"sort_numbers", "json_roundtrip", "join_strings"})
            self.assertTrue(all(r["seconds"] > 0 for r in rows))

    def test_gate_passes_on_baseline(self):
        proc = run("gate.py")
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("GATE OK", proc.stdout)

    def test_gate_catches_slowdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = os.path.join(tmp, "r.jsonl")
            base = os.path.join(tmp, "b.json")
            with open(runs, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"bench": "sort_numbers", "seconds": 0.002}) + "\n")
            with open(base, "w", encoding="utf-8") as fh:
                json.dump({"sort_numbers": 0.001}, fh)
            proc = run("gate.py", "--runs", runs, "--baseline", base, "--threshold", "10")
            self.assertEqual(proc.returncode, 1)
            self.assertIn("GATE FAIL", proc.stdout)

    def test_gate_reports_deltas(self):
        proc = run("gate.py")
        self.assertIn("delta=", proc.stdout)

    def test_trend_page_lists_benches(self):
        proc = run("trend.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        with open(os.path.join(ROOT, "trend.html"), encoding="utf-8") as fh:
            html = fh.read()
        for name in ("sort_numbers", "json_roundtrip", "join_strings"):
            self.assertIn(name, html)

    def test_baseline_covers_benches(self):
        with open(os.path.join(ROOT, "baseline.json"), encoding="utf-8") as fh:
            baseline = json.load(fh)
        self.assertEqual(set(baseline), {"sort_numbers", "json_roundtrip", "join_strings"})

    def test_runs_log_has_history(self):
        with open(os.path.join(ROOT, "runs.jsonl"), encoding="utf-8") as fh:
            self.assertGreaterEqual(len(fh.readlines()), 3)

    def test_update_baseline_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            runs = os.path.join(tmp, "r.jsonl")
            base = os.path.join(tmp, "b.json")
            with open(runs, "w", encoding="utf-8") as fh:
                fh.writelines(json.dumps({"bench": "sort_numbers", "seconds": 0.002}) + "\n" for _ in range(3))
            proc = run("gate.py", "--runs", runs, "--baseline", base, "--update-baseline")
            self.assertEqual(proc.returncode, 0)
            with open(base, encoding="utf-8") as fh:
                self.assertAlmostEqual(json.load(fh)["sort_numbers"], 0.002)


if __name__ == "__main__":
    unittest.main()
