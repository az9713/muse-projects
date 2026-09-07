# #5 Docs-to-code reproduction

A scaled-down stand-in for the "10k-line OpenAPI spec" task: same pipeline
shape (spec -> generator -> server + client + mocks -> contract tests), with
a compact 3-resource spec so the whole loop runs in seconds.

Pipeline:

```sh
python3 gen/generate.py   # spec/openapi.json -> out/server.py, out/client.py, out/mocks.py
```

`out/` is committed so the result is reviewable; CI regenerates and fails
on drift (`git diff --exit-code -- out/`).

## Verify (project env)

```sh
source .venv/bin/activate
python gen/generate.py
python -m pytest tests/ -q     # 10 passed
```

Contract: `tests/test_contract.py` runs the generated server in-process on
an ephemeral port and checks the generated client against it, with mock
payloads validated against the spec schemas. Stdlib only — no deps.
