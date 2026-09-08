# #17 Perf regression tracker

`bench.py` times hot functions into append-only `runs.jsonl`; `trend.py`
renders an offline `trend.html`; `gate.py` fails CI on >10% slowdown vs
`baseline.json` with a bisect hint.

```sh
source .venv/bin/activate
python bench.py                       # append a run
python trend.py                       # trend.html
python gate.py                        # GATE OK (or FAIL with bisect hint)
python gate.py --update-baseline      # re-baseline after intentional changes
python -m pytest tests/ -q            # 8 passed
```
