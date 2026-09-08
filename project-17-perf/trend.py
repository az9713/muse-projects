"""Trend page: last runs per bench as an offline HTML table + bars.

Usage: python3 trend.py [--runs FILE] [--out FILE]
"""
import argparse
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def load(runs_path):
    series = defaultdict(list)
    with open(runs_path, encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            series[row["bench"]].append(row["seconds"])
    return series


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", default=os.path.join(HERE, "runs.jsonl"))
    parser.add_argument("--out", default=os.path.join(HERE, "trend.html"))
    args = parser.parse_args(argv)
    series = load(args.runs)
    peak = max(max(v) for v in series.values())
    blocks = []
    for name in sorted(series):
        latest = series[name][-1]
        width = max(1, int(40 * latest / peak))
        blocks.append(f"<h2>{name}: {latest:.6f}s (n={len(series[name])})</h2><pre>{'#' * width}</pre>")
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Benchmark trend</title>"
        "<style>body{font-family:monospace;background:#161616;color:#e8e8e8;max-width:700px;margin:2rem auto}</style>"
        "</head><body><h1>Benchmark trend</h1>" + "\n".join(blocks) + "</body></html>"
    )
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
