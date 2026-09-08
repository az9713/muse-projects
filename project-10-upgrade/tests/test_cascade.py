"""Cascade tests: v2 lib behavior + all migrated callers (8 tests)."""
import os
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "vendor"))
sys.path.insert(0, os.path.join(ROOT, "pkgs", "billing"))
sys.path.insert(0, os.path.join(ROOT, "pkgs", "notify"))
sys.path.insert(0, os.path.join(ROOT, "pkgs", "cli"))

from billing import invoice_total
from cli import checkout
from lib import format_money, send
from notify import receipt


class CascadeTest(unittest.TestCase):
    def test_format_money_default(self):
        self.assertEqual(format_money(1999), "$19.99")

    def test_format_money_eur(self):
        self.assertIn("19.99", format_money(1999, "EUR"))

    def test_send_requires_channel(self):
        with self.assertRaises(TypeError):
            send("a@x.io", "hi")  # type: ignore[call-arg]

    def test_send_bad_channel(self):
        with self.assertRaises(ValueError):
            send("a@x.io", "hi", channel="fax")

    def test_billing_uses_v2(self):
        self.assertEqual(invoice_total([1000, 999]), "$19.99")

    def test_notify_wires_channel(self):
        out = receipt("a@x.io", "$19.99")
        self.assertEqual(out["channel"], "email")
        self.assertTrue(out["sent"])

    def test_cli_end_to_end(self):
        out = checkout("a@x.io", [1000, 999])
        self.assertEqual(out["to"], "a@x.io")
        self.assertIn("19.99", str(out["msg"]))

    def test_no_v1_imports_remain(self):
        sources = {
            "billing": os.path.join(ROOT, "pkgs", "billing", "billing.py"),
            "notify": os.path.join(ROOT, "pkgs", "notify", "notify.py"),
            "cli": os.path.join(ROOT, "pkgs", "cli", "cli.py"),
        }
        for name, path in sources.items():
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            self.assertNotIn("format_amount", body, name)
            self.assertNotIn("lib_v1", body, name)


if __name__ == "__main__":
    unittest.main()
