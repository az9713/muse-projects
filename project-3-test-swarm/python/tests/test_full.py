"""FULL suite (after the swarm): 23 tests over every branch. Also runs under pytest."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from billing import apply_discount, discount_rate, invoice, line_total, with_tax


class TestLineTotal(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(line_total(10.0, 3), 30.0)

    def test_zero_qty(self):
        self.assertEqual(line_total(10.0, 0), 0.0)

    def test_rounding(self):
        self.assertEqual(line_total(2.333, 3), 7.0)

    def test_negative_qty_raises(self):
        with self.assertRaises(ValueError):
            line_total(10.0, -1)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            line_total(-5.0, 2)


class TestDiscountRate(unittest.TestCase):
    def test_none(self):
        self.assertEqual(discount_rate(9), 0.0)

    def test_tier_10(self):
        self.assertEqual(discount_rate(10), 0.05)

    def test_tier_49(self):
        self.assertEqual(discount_rate(49), 0.05)

    def test_tier_50(self):
        self.assertEqual(discount_rate(50), 0.10)

    def test_tier_99(self):
        self.assertEqual(discount_rate(99), 0.10)

    def test_tier_100(self):
        self.assertEqual(discount_rate(100), 0.20)


class TestApplyDiscount(unittest.TestCase):
    def test_no_discount(self):
        self.assertEqual(apply_discount(100.0, 5), 100.0)

    def test_five_pct(self):
        self.assertEqual(apply_discount(100.0, 10), 95.0)

    def test_twenty_pct(self):
        self.assertEqual(apply_discount(200.0, 100), 160.0)


class TestWithTax(unittest.TestCase):
    def test_default_rate(self):
        self.assertEqual(with_tax(100.0), 107.0)

    def test_zero_rate(self):
        self.assertEqual(with_tax(100.0, 0.0), 100.0)

    def test_negative_rate_raises(self):
        with self.assertRaises(ValueError):
            with_tax(100.0, -0.01)


class TestInvoice(unittest.TestCase):
    def test_single_unit(self):
        inv = invoice(10.0, 1)
        self.assertEqual(inv["subtotal"], 10.0)
        self.assertEqual(inv["discount"], 0.0)
        self.assertEqual(inv["total"], 10.7)

    def test_bulk_discount_applied(self):
        inv = invoice(10.0, 100)
        self.assertEqual(inv["subtotal"], 1000.0)
        self.assertEqual(inv["discount"], 200.0)
        self.assertEqual(inv["total"], 856.0)

    def test_zero_qty(self):
        inv = invoice(10.0, 0)
        self.assertEqual(inv, {"subtotal": 0.0, "discount": 0.0, "total": 0.0})

    def test_custom_tax(self):
        inv = invoice(100.0, 1, rate=0.0)
        self.assertEqual(inv["total"], 100.0)

    def test_mid_tier(self):
        inv = invoice(20.0, 50)
        self.assertEqual(inv["subtotal"], 1000.0)
        self.assertEqual(inv["discount"], 100.0)

    def test_keys(self):
        self.assertEqual(set(invoice(5.0, 2).keys()), {"subtotal", "discount", "total"})


if __name__ == "__main__":
    unittest.main()
