# #9 Traffic-to-SDK

`traffic/access.log` (17 requests, 5 endpoint shapes incl. 404s) plus
`traffic/samples.json` go in; `gen/build_sdk.py` infers endpoints — numeric
segments fold to `{id}` — and emits a transport-injectable `out/client.py`.

## Verify (project env)

```sh
source .venv/bin/activate
python gen/build_sdk.py          # 5 endpoints inferred
python -m pytest tests/ -q       # 10 passed
```

The client takes a `transport` callable, so the suite runs with zero network.
