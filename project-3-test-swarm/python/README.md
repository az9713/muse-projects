# #3 Test-and-fix swarm — Python (`billing.py`)

Weak suite: `tests/test_weak.py` (2 tests, thin coverage).
Full suite: `tests/test_full.py` (23 tests, every branch + edge cases).

## Verify (project env)

```sh
cd python
source .venv/bin/activate
python -m unittest tests.test_weak -v    # before: thin
python -m unittest tests.test_full -v    # after: full
python -m pytest tests/test_full.py -q   # also pytest-compatible
```

The swarm story: generate the full suite from the weak one, then fix
every failure it surfaces. Here the full suite is green against the
current `billing.py` — the demo artifact is the suite itself.
