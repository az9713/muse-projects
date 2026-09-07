# #1 Migration runner (both minimal)

Two samples of the same mechanical migration shape (every file touched, re-run green):

- `python-sample/` — unittest -> pytest. Env in `python-sample/.venv`
  (`source .venv/bin/activate`). See its README.
- `js-sample/` — CommonJS -> ESM (dependency-free stand-in for Jest->Vitest,
  same multi-file rewrite shape). See its README.

Nothing was deleted; `muse.png` and `muse-token-heavy-projects.html` untouched.
