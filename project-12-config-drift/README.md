# #12 Config drift doctor

`envs/` holds three drifted environment files (the committed `SECRET_KEY`
is a clearly-marked fake for the demo). `doctor.py` diffs them, flags drift
and the committed secret, and emits a unified schema:

```sh
source .venv/bin/activate
python doctor.py                       # 6 findings: F1..F6
python -m pytest tests/ -q             # 8 passed
```

Outputs: `findings.json` (ids + severities), `schema.json` (required keys,
types, rules), `.env.example` (secret-free template).
