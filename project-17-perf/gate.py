"""CI gate: fail when the latest run regresses > threshold vs baseline.

Usage: python3 gate.py [--runs FILE] [--baseline FILE] [--threshold PCT]
       python3 gate.py --update-baseline   (record current means as baseline)
"""
import argparse
import json
import os
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def means(runs_path):
    series = defaultdict(list)
    with open(runs_path, encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            series[row["bench"]].append(row["seconds"])
    return {name: statistics.mean(values[-3:]) for name, values in series.items()}


def check(runs_path, baseline_path, threshold):
    with open(baseline_path, encoding="utf-8") as fh:
        baseline = json.load(fh)
    current = means(runs_path)
    failed = []
    for name, base in baseline.items():
        now = current[name]
        delta = (now - base) / base * 100
        print(f"{name}: baseline={base:.6f}s now={now:.6f}s delta={delta:+.1f}%")
        if delta > threshold:
            failed.append(name)
    if failed:
        print(f"GATE FAIL: regressed > {threshold}%: {failed} (bisect hint: rerun bench.py per-bench)")
        return 1
    print("GATE OK")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", default=os.path.join(HERE, "runs.jsonl"))
    parser.add_argument("--baseline", default=os.path.join(HERE, "baseline.json"))
    parser.add_argument("--threshold", type=float, default=10.0)
    parser.add_argument("--update-baseline", action="store_true")
    args = parser.parse_args(argv)
    if args.update_baseline:
        with open(args.baseline, "w", encoding="utf-8") as fh:
            json.dump(means(args.runs), fh, indent=2)
        print(f"wrote {args.baseline}")
        return 0
    return check(args.runs, args.baseline, args.threshold)


if __name__ == "__main__":
    sys.exit(main())
