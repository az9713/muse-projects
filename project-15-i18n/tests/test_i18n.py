"""i18n tests: fallback, interpolation, guard (8 tests)."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from app.i18n import t
from app.views import farewell, greeting, inbox
from tools.check import used_keys


class I18nTest(unittest.TestCase):
    def test_english(self):
        self.assertEqual(greeting("en", "Ann"), "Hello, Ann!")

    def test_spanish(self):
        self.assertEqual(greeting("es", "Ann"), "¡Hola, Ann!")

    def test_fallback_to_english(self):
        self.assertEqual(inbox("es", 3), "You have 3 messages.")

    def test_unknown_locale_falls_back(self):
        self.assertEqual(greeting("xx", "Ann"), "Hello, Ann!")

    def test_missing_key_returns_key(self):
        self.assertEqual(t("nope", "en"), "nope")

    def test_interpolation(self):
        self.assertEqual(farewell("en", "Bo"), "Goodbye, Bo.")

    def test_guard_passes(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "tools", "check.py")],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn("missing=0", proc.stdout)

    def test_used_keys_match_en(self):
        self.assertEqual(used_keys(), {"hello", "bye", "inbox"})


if __name__ == "__main__":
    unittest.main()
