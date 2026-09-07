"""Tests for the polyglot scaffolder (12 tests)."""
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cli"))

from scaffold import LANGS, scaffold


class ScaffoldTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def _scaffold(self, lang, name="demo"):
        return scaffold(lang, name, self.tmp.name)

    def test_all_langs_known(self):
        self.assertEqual(tuple(LANGS), ("ts", "go", "rust"))

    def test_unknown_lang_raises(self):
        with self.assertRaises(ValueError):
            scaffold("zig", "demo", self.tmp.name)

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            scaffold("ts", "  ", self.tmp.name)

    def test_ts_tree(self):
        target = self._scaffold("ts")
        for rel in ("package.json", "src/index.mjs", "test/index.test.mjs"):
            self.assertTrue(os.path.isfile(os.path.join(target, rel)), rel)

    def test_ts_package_json_valid(self):
        with open(os.path.join(self._scaffold("ts"), "package.json")) as fh:
            pkg = json.load(fh)
        self.assertEqual(pkg["type"], "module")
        self.assertIn("test", pkg["scripts"])

    def test_ts_greeting_wired(self):
        target = self._scaffold("ts", "myapp")
        with open(os.path.join(target, "test/index.test.mjs")) as fh:
            body = fh.read()
        self.assertIn("hello from myapp", body)

    def test_go_tree(self):
        target = self._scaffold("go")
        for rel in ("go.mod", "main.go", "main_test.go"):
            self.assertTrue(os.path.isfile(os.path.join(target, rel)), rel)

    def test_go_module_name(self):
        with open(os.path.join(self._scaffold("go", "svc"), "go.mod")) as fh:
            self.assertIn("module svc", fh.read())

    def test_go_test_matches_impl(self):
        target = self._scaffold("go", "svc")
        with open(os.path.join(target, "main.go")) as fh:
            impl = fh.read()
        with open(os.path.join(target, "main_test.go")) as fh:
            test = fh.read()
        self.assertIn("hello from svc", impl)
        self.assertIn("hello from svc", test)

    def test_rust_tree(self):
        target = self._scaffold("rust")
        for rel in ("Cargo.toml", "src/main.rs"):
            self.assertTrue(os.path.isfile(os.path.join(target, rel)), rel)

    def test_rust_manifest_and_test(self):
        target = self._scaffold("rust", "tool")
        with open(os.path.join(target, "Cargo.toml")) as fh:
            self.assertIn('name = "tool"', fh.read())
        with open(os.path.join(target, "src/main.rs")) as fh:
            body = fh.read()
        self.assertIn("hello from tool", body)
        self.assertIn("#[test]", body)

    def test_target_dir_named(self):
        target = self._scaffold("rust", "tool")
        self.assertTrue(target.endswith("tool-rust"))


if __name__ == "__main__":
    unittest.main()
