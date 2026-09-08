"""Parse logs/access.log -> report.db (SQLite) + report.html (single file).

Usage: python3 analyze.py
Answers: total requests, error rate, p50/p95 latency overall + per path,
top paths, slowest-path ranking, hourly error spike.
"""
import os
import sqlite3
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "logs", "access.log")
DB = os.path.join(HERE, "report.db")
HTML = os.path.join(HERE, "report.html")


def parse():
    rows = []
    with open(LOG, encoding="utf-8") as fh:
        for line in fh:
            ip, ts, method, path, status, latency = line.split()
            rows.append((ip, int(ts), method, path, int(status), int(latency)))
    return rows


def percentile(values, pct):
    if not values:
        return 0
    ordered = sorted(values)
    rank = min(len(ordered) - 1, int(len(ordered) * pct / 100))
    return ordered[rank]


def build_db(rows):
    if os.path.exists(DB):
        os.remove(DB)
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE requests (ip, ts, method, path, status, latency_ms)")
    con.executemany("INSERT INTO requests VALUES (?,?,?,?,?,?)", rows)
    con.commit()
    return con


def summarize(con):
    total = con.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    errors = con.execute("SELECT COUNT(*) FROM requests WHERE status >= 500").fetchone()[0]
    lats = [r[0] for r in con.execute("SELECT latency_ms FROM requests")]
    paths = con.execute(
        "SELECT path, COUNT(*), AVG(latency_ms) FROM requests GROUP BY path ORDER BY COUNT(*) DESC"
    ).fetchall()
    per_path_p95 = {}
    for (path,) in con.execute("SELECT DISTINCT path FROM requests"):
        vals = [r[0] for r in con.execute("SELECT latency_ms FROM requests WHERE path = ?", (path,))]
        per_path_p95[path] = percentile(vals, 95)
    hours = con.execute(
        "SELECT (ts / 3600) * 3600 AS h, SUM(status >= 500) FROM requests GROUP BY h ORDER BY h"
    ).fetchall()
    return {
        "total": total,
        "errors": errors,
        "p50": percentile(lats, 50),
        "p95": percentile(lats, 95),
        "mean": round(statistics.mean(lats), 1),
        "paths": paths,
        "per_path_p95": per_path_p95,
        "hours": hours,
    }


def render(summary):
    rows = "\n".join(
        f"<tr><td>{p}</td><td>{n}</td><td>{a:.1f}</td><td>{summary['per_path_p95'][p]}</td></tr>"
        for p, n, a in summary["paths"]
    )
    peak = max(summary["hours"], key=lambda h: h[1])
    scale = max(h[1] for h in summary["hours"]) or 1
    bars = "\n".join(
        f"<div>{h} errors={e} {'#' * max(1, int(40 * e / scale))}</div>" for h, e in summary["hours"]
    )
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Traffic report</title>
<style>body{{font-family:monospace;background:#161616;color:#e8e8e8;max-width:800px;margin:2rem auto;padding:0 1rem}}
table{{border-collapse:collapse}}td,th{{border:1px solid #444;padding:.3rem .6rem}}</style>
</head><body>
<h1>Traffic report</h1>
<p>requests={summary['total']} errors={summary['errors']} p50={summary['p50']}ms
p95={summary['p95']}ms mean={summary['mean']}ms</p>
<h2>Per path (requests, avg ms, p95 ms)</h2>
<table><tr><th>path</th><th>n</th><th>avg</th><th>p95</th></tr>{rows}</table>
<h2>Errors per hour (peak {peak[0]} with {peak[1]})</h2>
<pre>{bars}</pre>
</body></html>
"""


def main():
    rows = parse()
    con = build_db(rows)
    summary = summarize(con)
    con.close()
    with open(HTML, "w", encoding="utf-8") as fh:
        fh.write(render(summary))
    print(f"requests={summary['total']} errors={summary['errors']} p50={summary['p50']} p95={summary['p95']}")
    print("wrote report.db + report.html")


if __name__ == "__main__":
    main()
