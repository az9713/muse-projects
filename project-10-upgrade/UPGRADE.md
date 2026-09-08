# #10 Upgrade cascade — vendor lib v1 → v2 across 3 packages

`vendor/lib_v1.py` is the frozen before-state. `vendor/lib.py` (v2) made two
breaking changes; `pkgs/{billing,notify,cli}` were migrated caller by caller.

## Breakages hit (in order)

1. `billing`: `format_amount` gone → `NameError` → switched to
   `format_money(sum, currency)`, keeping USD default.
2. `notify`: `send(to, msg)` → `TypeError: missing channel` → explicit
   `channel="email"` at the call site (chosen over a default: explicit routing).
3. `cli`: green once both deps migrated — no direct change needed.

## Verify (project env)

```sh
source .venv/bin/activate
python -m pytest tests/ -q     # 8 passed
```
