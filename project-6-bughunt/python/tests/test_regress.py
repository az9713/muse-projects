"""Regression tests: assert CORRECT behavior (fail on buggy code, pass fixed)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

os.environ.pop("APP_DEBUG", None)

from orders import add_note, bulk_rate, line_total, promo_active, receipt


class TestFixed(unittest.TestCase):
    def test_b1_boundary(self):
        self.assertEqual(bulk_rate(99), 0.10)
        self.assertEqual(bulk_rate(100), 0.20)
        self.assertEqual(bulk_rate(101), 0.20)

    def test_b2_no_shared_default(self):
        self.assertEqual(add_note("a"), ["a"])
        self.assertEqual(add_note("b"), ["b"])

    def test_b3_money_exact(self):
        self.assertEqual(line_total(0.1, 3), 0.3)
        self.assertEqual(line_total(2.33, 3), 6.99)

    def test_b4_no_cost_leak(self):
        self.assertNotIn("cost", receipt("widget", 1))

    def test_b4_debug_still_no_cost(self):
        os.environ["APP_DEBUG"] = "1"
        try:
            self.assertNotIn("cost", receipt("widget", 1))
        finally:
            os.environ.pop("APP_DEBUG", None)

    def test_b5_year_boundary(self):
        self.assertTrue(promo_active("12/30/2026"))
        self.assertTrue(promo_active("01/05/2026"))
        self.assertFalse(promo_active("01/05/2027"))

    def test_receipt_total(self):
        self.assertEqual(receipt("widget", 100)["total"], 800.0)


if __name__ == "__main__":
    unittest.main()
