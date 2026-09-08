"""Micro-benchmarks: time hot functions, append JSONL rows to runs.jsonl.

Usage: python3 bench.py [--runs FILE] [--repeat N]
"""
import argparse
import json
import os
import timeit

HERE = os.path.dirname(os.path.abspath(__file__))


def sort_numbers():
    sorted(range(5000, 0, -1))


def json_roundtrip():
    import json as j

    payload = {"items": [{"id": i, "name": f"n{i}"} for i in range(200)]}
    j.loads(j.dumps(payload))


def join_strings():
    ",".join(f"row{i}" for i in range(2000))


BENCHES = {"sort_numbers": sort_numbers, "json_roundtrip": json_roundtrip, "join_strings": join_strings}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", default=os.path.join(HERE, "runs.jsonl"))
    parser.add_argument("--repeat", type=int, default=5)
    args = parser.parse_args(argv)
    with open(args.runs, "a", encoding="utf-8") as fh:
        for name, func in BENCHES.items():
            seconds = min(timeit.repeat(func, number=1, repeat=args.repeat))
            fh.write(json.dumps({"bench": name, "seconds": round(seconds, 6)}) + "\n")
            print(f"{name}: {seconds:.6f}s")
    print(f"appended to {args.runs}")


if __name__ == "__main__":
    main()
