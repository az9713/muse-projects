"""Parser tests: examples + seeded round-trip property (10 tests)."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fuzz import random_fields
from parser import join_row, parse_line


class ParserTest(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_line("a,b,c"), ["a", "b", "c"])

    def test_quoted_comma(self):
        self.assertEqual(parse_line('"x,y",z'), ["x,y", "z"])

    def test_escaped_quote(self):
        self.assertEqual(parse_line('"say ""hi""",ok'), ['say "hi"', "ok"])

    def test_empty_fields(self):
        self.assertEqual(parse_line("a,,c"), ["a", "", "c"])

    def test_trailing_comma(self):
        self.assertEqual(parse_line("a,b,"), ["a", "b", ""])

    def test_join_quotes(self):
        self.assertEqual(join_row(["x,y", "z"]), '"x,y",z')

    def test_join_escapes(self):
        self.assertEqual(join_row(['say "hi"']), '"say ""hi"""')

    def test_round_trip_property(self):
        rng = random.Random(14)
        for _ in range(200):
            fields = random_fields(rng)
            self.assertEqual(parse_line(join_row(fields)), fields)

    def test_single_empty(self):
        self.assertEqual(parse_line(""), [""])

    def test_findings_log_ends_green(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "findings.log"), encoding="utf-8") as fh:
            tail = fh.read().strip().splitlines()[-1]
        self.assertIn("5000/5000 ok", tail)


if __name__ == "__main__":
    unittest.main()
