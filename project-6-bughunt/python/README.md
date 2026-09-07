# #6 Bug-hunt — Python (`src/orders.py`, bugs B1..B5, all fixed)

## Verify (project env)

```sh
cd python
source .venv/bin/activate
python repro/repro.py          # 5/5
python -m pytest tests/ -q     # 7 passed
```

History: `proof/before-fix.log` (0/5 red) -> fixes -> `proof/after-fix.log`
(5/5 green). Fix details in `../SOLUTIONS.md`.
