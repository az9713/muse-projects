"""WEAK suite (before the swarm): only 2 tests. Run: python3 -m unittest tests.test_weak -v"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from billing import invoice


class TestWeak(unittest.TestCase):
    def test_basic_invoice(self):
        inv = invoice(10.0, 1)
        self.assertEqual(inv["subtotal"], 10.0)

    def test_total_above_subtotal_with_tax(self):
        inv = invoice(10.0, 1)
        self.assertGreater(inv["total"], 0)


if __name__ == "__main__":
    unittest.main()
