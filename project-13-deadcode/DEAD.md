# #13 Dead-code census

`census.py` finds module-level functions/classes with no importer in the
tree (entry module `app` counts as roots). `src/` is post-census clean;
`fixtures/` keeps planted dead code so the tool stays testable.

Removed during the census (verified with `grep -r`, suite re-run green):

- `src/utils.py::orphan()` — no importers
- `src/models.py::LegacyRecord` — no importers
- `src/dead_mod.py` — whole module unreferenced

## Verify (project env)

```sh
source .venv/bin/activate
python census.py src            # 0 dead symbols
python census.py fixtures       # 3 dead symbols
python -m pytest tests/ -q     # 8 passed
```
