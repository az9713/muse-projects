#!/bin/sh
# heal.sh — run every check the CI runs, locally. Fails loud, fixes what it can.
# Usage: sh heal.sh   (from the repo root)
set -u
fail=0
note() { echo "== $1"; }

PY_PROJS="project-1-migration/python-sample project-2-coldstart/python project-3-test-swarm/python project-4-polyglot project-5-docs-to-code project-6-bughunt/python"
for proj in $PY_PROJS; do
  tdir="$proj/tests"
  if [ ! -x "$proj/.venv/bin/python" ]; then
    note "$proj: creating .venv"
    (cd "$proj" && (uv venv || python3 -m venv .venv)) || { echo "FAIL $proj: venv"; fail=1; continue; }
  fi
  if ! "$proj/.venv/bin/python" -m pytest --version >/dev/null 2>&1; then
    (cd "$proj" && (uv pip install --python .venv/bin/python pytest || .venv/bin/pip install pytest)) \
      || { echo "FAIL $proj: pytest install"; fail=1; continue; }
  fi
  if "$proj/.venv/bin/python" -m pytest "$tdir" -q 2>&1 | tail -2; then
    echo "PASS $proj"
  else
    echo "FAIL $proj"; fail=1
  fi
done

note "regen check (#5)"
project-5-docs-to-code/.venv/bin/python project-5-docs-to-code/gen/generate.py
if git diff --quiet -- project-5-docs-to-code/out 2>/dev/null; then
  echo "PASS regen: out/ fresh"
else
  echo "FAIL regen: out/ drifted (commit the regenerated files)"; fail=1
fi

note "node suites"
for t in "node project-1-migration/js-sample/test/test-legacy.cjs" \
         "node --test project-1-migration/js-sample/test/test-migrated.test.mjs" \
         "node --test project-2-coldstart/js/test/tags.test.mjs" \
         "node project-3-test-swarm/js/test/test-weak.mjs" \
         "node --test project-3-test-swarm/js/test/test-full.test.mjs" \
         "sh project-4-polyglot/e2e/check.sh" \
         "node project-6-bughunt/js/repro/repro.mjs" \
         "node --test project-6-bughunt/js/test/regress.test.mjs"; do
  if $t >/dev/null 2>&1; then echo "PASS $t"; else echo "FAIL $t"; fail=1; fi
done

note "lint (ruff, auto-fix)"
if uvx ruff check --fix . 2>&1 | tail -2 && uvx ruff check . 2>&1 | tail -2; then
  echo "PASS ruff"
else
  echo "WARN ruff unavailable or failing (see above)"; fail=1
fi

if [ "$fail" = 0 ]; then echo "HEALED: all green"; else echo "HEAL FAILED"; fi
exit "$fail"
