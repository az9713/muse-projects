# #11 Log-to-dashboard

`gen_logs.py` synthesizes 2000 deterministic log lines (seed 20260907).
`analyze.py` parses them into `report.db` (SQLite) and renders a single-file
`report.html`: totals, p50/p95, per-path table, hourly error bars.

## Verify (project env)

```sh
source .venv/bin/activate
python gen_logs.py                   # logs/access.log (regenerable)
python analyze.py                    # report.db + report.html
python -m pytest tests/ -q           # 8 passed
```

`tests/test_report.py` re-parses the log independently and asserts the db
and html agree (row counts, error counts, p95, rankings).
