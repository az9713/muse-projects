#!/bin/sh
# E2E: scaffold all three languages, verify trees, run real toolchains if present.
set -u
CLI_DIR=$(dirname "$0")/../cli
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

fail=0
for lang in ts go rust; do
  target=$(python3 "$CLI_DIR/scaffold.py" --lang "$lang" --name e2e --out "$WORK")
  [ -d "$target" ] || { echo "FAIL $lang: no output dir"; fail=1; continue; }
  echo "PASS $lang: scaffolded to $target"
done

# Real toolchain checks: opportunistic, skipped when the toolchain is absent.
if command -v node >/dev/null 2>&1; then
  node --check "$WORK/e2e-ts/src/index.mjs" && echo "PASS ts: node --check" || fail=1
  (cd "$WORK/e2e-ts" && node --test test/index.test.mjs 2>&1 | grep -q "# fail 0") \
    && echo "PASS ts: generated tests run" || { echo "FAIL ts: generated tests"; fail=1; }
else
  echo "SKIP ts toolchain checks (no node)"
fi
if command -v go >/dev/null 2>&1; then
  (cd "$WORK/e2e-go" && go test ./...) && echo "PASS go: go test" || { echo "FAIL go test"; fail=1; }
else
  echo "SKIP go toolchain checks (no go)"
fi
if command -v cargo >/dev/null 2>&1; then
  (cd "$WORK/e2e-rust" && cargo test --quiet) && echo "PASS rust: cargo test" || { echo "FAIL cargo test"; fail=1; }
else
  echo "SKIP rust toolchain checks (no cargo)"
fi

if [ "$fail" = 0 ]; then echo "E2E OK"; else echo "E2E FAILED"; fi
exit "$fail"
