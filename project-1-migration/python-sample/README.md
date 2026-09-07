# #1 Migration runner — Python sample (unittest -> pytest)

Legacy: `tests/test_legacy_unittest.py` (TestCase classes).
Migrated: `tests/test_migrated_pytest.py` (plain asserts, fixture, parametrize).

## Verify (project env, pytest installed)

```sh
cd python-sample
source .venv/bin/activate
python -m unittest discover -s tests -p 'test_legacy_unittest.py' -t .  # legacy: 12 pass
python -m pytest tests/test_migrated_pytest.py -v                       # migrated: 15 pass
python3 check_parity.py                                                  # stdlib parity: 10 checks
```

`check_parity.py` exercises the same cases as both suites so behavior
parity is proven even where `pytest` is not installed yet.
