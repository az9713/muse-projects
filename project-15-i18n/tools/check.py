"""CI guard: every t() key used in views must exist in en.json.

Usage: python3 tools/check.py  (exit 1 on missing keys; extra keys reported)
"""
import ast
import json
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def used_keys():
    with open(os.path.join(ROOT, "app", "views.py"), encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    keys = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and getattr(node.func, "id", "") == "t"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        ):
            keys.add(node.args[0].value)
    return keys


def main():
    with open(os.path.join(ROOT, "app", "locale", "en.json"), encoding="utf-8") as fh:
        en = json.load(fh)
    with open(os.path.join(ROOT, "app", "locale", "es.json"), encoding="utf-8") as fh:
        es = json.load(fh)
    required = used_keys()
    missing = sorted(required - set(en))
    extra = sorted(set(en) - required)
    uncovered = sorted(set(en) - set(es))
    for key in missing:
        print(f"MISSING en: {key}")
    for key in extra:
        print(f"note: unused en key: {key}")
    for key in uncovered:
        print(f"note: es falls back to en: {key}")
    print(f"keys used={len(required)} missing={len(missing)}")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
