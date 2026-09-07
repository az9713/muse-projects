# #6 Bug-hunt marathon (5 Python + 5 JS)

Two small apps, each with 5 injected bugs: off-by-one, shared mutable
state, numeric drift, env/config leak, and date/async/coercion traps.

## Hunt protocol (for scoring another agent)

1. Run the repro: `python3 repro/repro.py` / `node repro/repro.mjs`
   (expect 0/5 on the buggy originals).
2. Fix until 5/5. Log each in `BUGLOG.md`.
3. Confirm regression suites still pass (7 + 5 tests).
4. Only then open `SOLUTIONS.md` to score.

Reference (already done here, with proof logs in `proof/`):

```sh
cd python && source .venv/bin/activate && python -m pytest tests/ -q
cd ../js && node --test test/regress.test.mjs
```
