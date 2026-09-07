# #2 Cold-start feature — Python task tracker

A small layered app (`tasks/store.py` -> `tasks/service.py` ->
`tasks/cli.py`, docs in `docs/API.md`). The agent was handed only
`TASK.md` and implemented tags across all layers.

## Verify (project env)

```sh
cd python
uv venv  # first time only (or: python3 -m venv .venv)
source .venv/bin/activate
python -m unittest discover -s tests -v
```

Acceptance: `tests/test_tags.py`, 10 tests.
