"""Doctor tests: 6 findings + schema behavior (8 tests)."""
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, ROOT)

from doctor import doctor, parse, validate


class DoctorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.findings = {f["id"]: f for f in doctor()}
        with open(os.path.join(ROOT, "schema.json"), encoding="utf-8") as fh:
            cls.schema = json.load(fh)

    def test_six_findings(self):
        self.assertEqual(set(self.findings), {"F1", "F2", "F3", "F4", "F5", "F6"})

    def test_secret_is_critical(self):
        self.assertEqual(self.findings["F4"]["severity"], "critical")
        self.assertIn("prod.env", self.findings["F4"]["detail"])

    def test_missing_retries_high(self):
        self.assertEqual(self.findings["F2"]["severity"], "high")

    def test_schema_validates_dev(self):
        self.assertEqual(validate(parse(os.path.join(ROOT, "envs", "dev.env"))), [])

    def test_schema_catches_prod(self):
        errors = validate(parse(os.path.join(ROOT, "envs", "prod.env")))
        self.assertTrue(any("RETRIES" in e for e in errors))

    def test_schema_rejects_bad_type(self):
        self.assertTrue(any("TIMEOUT" in e for e in validate({"TIMEOUT": "soon"})))

    def test_example_has_no_secrets(self):
        with open(os.path.join(ROOT, ".env.example"), encoding="utf-8") as fh:
            body = fh.read()
        self.assertNotIn("SECRET", body)
        for key in self.schema["required"]:
            self.assertIn(key, body)

    def test_findings_json_matches(self):
        with open(os.path.join(ROOT, "findings.json"), encoding="utf-8") as fh:
            on_disk = {f["id"]: f for f in json.load(fh)}
        self.assertEqual(on_disk, self.findings)


if __name__ == "__main__":
    unittest.main()
