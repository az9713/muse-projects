"""Parity check: runs without pytest. Exercises the same cases as both suites."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from calc import add, sub, mul, div
from strings import slugify, truncate, count_words
from stats import mean, clamp, pct_change

checks = [
    ("add", add(2, 3) == 5),
    ("sub", sub(5, 3) == 2),
    ("mul", mul(3, 4) == 12),
    ("div", abs(div(7, 2) - 3.5) < 1e-9),
    ("slugify", slugify("Hello World") == "hello-world"),
    ("truncate_short", truncate("abc", 10) == "abc"),
    ("count_words", count_words("a b c") == 3),
    ("mean", abs(mean([1, 2, 3, 4]) - 2.5) < 1e-9),
    ("clamp", clamp(10, 0, 5) == 5 and clamp(-1, 0, 5) == 0),
    ("pct_change", abs(pct_change(100, 120) - 20.0) < 1e-9),
]

failed = [name for name, ok in checks if not ok]

try:
    div(1, 0)
    failed.append("div_zero_should_raise")
except ValueError:
    pass

try:
    mean([])
    failed.append("mean_empty_should_raise")
except ValueError:
    pass

if failed:
    print("PARITY FAIL:", ", ".join(failed))
    sys.exit(1)
print(f"PARITY OK: {len(checks)} checks passed")
