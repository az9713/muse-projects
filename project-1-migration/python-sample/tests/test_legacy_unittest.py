"""LEGACY suite: unittest style (before migration). Run: python3 -m unittest discover -s tests -p 'test_*unittest.py' -t ."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from calc import add, div, mul, sub
from stats import clamp, mean, pct_change
from strings import count_words, slugify, truncate


class TestCalc(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)

    def test_mul(self):
        self.assertEqual(mul(3, 4), 12)

    def test_div(self):
        self.assertAlmostEqual(div(7, 2), 3.5)

    def test_div_zero(self):
        with self.assertRaises(ValueError):
            div(1, 0)


class TestStrings(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_truncate_short(self):
        self.assertEqual(truncate("abc", 10), "abc")

    def test_count_words(self):
        self.assertEqual(count_words("a b c"), 3)


class TestStats(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3]), 2.0)

    def test_mean_empty(self):
        with self.assertRaises(ValueError):
            mean([])

    def test_clamp(self):
        self.assertEqual(clamp(10, 0, 5), 5)

    def test_pct_change(self):
        self.assertAlmostEqual(pct_change(100, 120), 20.0)


if __name__ == "__main__":
    unittest.main()
