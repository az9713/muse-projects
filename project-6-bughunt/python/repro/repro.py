"""Repro script: one check per injected bug. Exit 1 if any FAIL."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

os.environ.pop("APP_DEBUG", None)  # hunter runs with a clean env

from orders import add_note, bulk_rate, line_total, promo_active, receipt

results = []


def check(name, cond):
    results.append((name, cond))
    print(("PASS" if cond else "FAIL"), name)


check("B1 bulk_rate(100) == 0.20", bulk_rate(100) == 0.20)
check("B2 add_note isolated", add_note("a") == ["a"] and add_note("b") == ["b"])
check("B3 line_total(0.1, 3) == 0.3", line_total(0.1, 3) == 0.3)
check("B4 receipt hides cost by default", "cost" not in receipt("widget", 1))
check("B5 promo over year boundary", promo_active("01/05/2026") and not promo_active("01/05/2027"))

failed = [n for n, ok in results if not ok]
print(f"{len(results) - len(failed)}/{len(results)} passed")
sys.exit(1 if failed else 0)
