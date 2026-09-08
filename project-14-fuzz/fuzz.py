"""Property fuzzer: random rows must survive join -> parse round-trip.

Usage: python3 fuzz.py [count]  (default 5000, seed fixed)
Exit 1 on any mismatch/crash; prints first failures.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import join_row, parse_line

ALPHABET = ["a", "bc", "", " ", ",", '"', 'say "hi"', "x,y", "trail,", '""']


def random_fields(rng):
    return [rng.choice(ALPHABET) for _ in range(rng.randint(1, 5))]


def main(argv=None):
    count = int((argv or sys.argv[1:])[0:1][0] if (argv or sys.argv[1:]) else 5000)
    rng = random.Random(14)
    fails = []
    for i in range(count):
        fields = random_fields(rng)
        line = join_row(fields)
        try:
            got = parse_line(line)
        except Exception as exc:  # noqa: BLE001 — fuzzer records everything
            fails.append((fields, line, f"CRASH {exc!r}"))
            continue
        if got != fields:
            fails.append((fields, line, f"got {got!r}"))
        if len(fails) >= 5:
            break
    for fields, line, why in fails:
        print(f"FAIL fields={fields!r} line={line!r} {why}")
    print(f"{count - len(fails)}/{count} ok")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
