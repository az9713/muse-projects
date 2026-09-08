# #16 Migration rehearsal

`migrate.py` steps SQLite v1 → v2 → v3 (backfill + new table) with a
rollback for every step. `rehearse.py` proves migrate → verify → rollback →
verify on a seeded database and writes `REHEARSAL.log`.

```sh
source .venv/bin/activate
python rehearse.py                  # REHEARSAL OK, users byte-identical
python -m pytest tests/ -q          # 8 passed
```
