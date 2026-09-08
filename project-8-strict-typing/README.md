# #8 Strict typing ascent — Python (`mypy --strict`)

`before/` is the untyped starting point (frozen). `app/` is the same code
fully annotated: dataclass model, typed persistence with explicit JSON
narrowing, typed service layer.

## Verify (project env)

```sh
source .venv/bin/activate
mypy app                 # Success: no issues found
python -m pytest tests/ -q   # 10 passed
```

## Ascent log

1. `models.py`: class → `@dataclass`, `tags=None` → `list[str] | None`,
   validation moved into `new_task` (empty titles now raise).
2. `store.py`: `t.__dict__` dump → `dataclasses.asdict`; `Task(**row)`
   → explicit per-field construction with `isinstance` narrowing.
3. `service.py`: full signatures; `complete()` added (was missing).
4. `mypy --strict` iterated to zero errors; behavior pinned by `tests/`.
