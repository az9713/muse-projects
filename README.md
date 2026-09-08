# Muse Projects — coding showcases

**Live guide: https://az9713.github.io/muse-projects/**

Seven small, self-contained projects demonstrating agentic coding workflows:
multi-file migrations, cold-start feature work, test generation, polyglot
scaffolding, docs-to-code generation, bug hunting, and self-healing CI.

| # | Project | What it is |
|---|---------|------------|
| 1 | `project-1-migration` | Repo-wide migration runner (unittest→pytest, CommonJS→ESM) |
| 2 | `project-2-coldstart` | Cold-start feature: tags across a layered task tracker |
| 3 | `project-3-test-swarm` | Test-and-fix swarm: weak suite expanded to full coverage |
| 4 | `project-4-polyglot` | One Python CLI scaffolds TS, Go, and Rust projects |
| 5 | `project-5-docs-to-code` | OpenAPI spec → server + client + mocks + contract tests |
| 6 | `project-6-bughunt` | Bug-hunt marathon: 10 injected bugs with repro + fixes |
| 7 | `heal.sh` + `docker/` | Self-healing CI: whole repo green in one command |
| 8 | `project-8-strict-typing` | Untyped code → `mypy --strict` clean, tests green |
| 9 | `project-9-traffic-sdk` | Access log → inferred endpoints → tested client |
| 10 | `project-10-upgrade` | Vendor lib v1 → v2 breakages chased across 3 packages |
| 11 | `project-11-log-dashboard` | 2000 log lines → SQLite + offline HTML report |
| 12 | `project-12-config-drift` | Drifted envs → findings + unified schema |
| 13 | `project-13-deadcode` | AST census: dead code removed with green proof |
| 14 | `project-14-fuzz` | 5000-case fuzz round-trip on a CSV parser |
| 15 | `project-15-i18n` | UI strings → locales + fallback + CI guard |
| 16 | `project-16-rehearsal` | SQLite migration with proven rollback |
| 17 | `project-17-perf` | Benchmarks + trend page + regression gate |

## Prerequisites

- Python 3.10+ with [`uv`](https://docs.astral.sh/uv/) (or plain `venv`+`pip`)
- Node.js 22+ (stdlib only — no `npm install` needed anywhere)
- Optional: `go`, `cargo` (unlock extra e2e checks in #4), Docker (for #7 image)

Each Python project keeps its own `.venv` (created on first use).

## 1 — Migration runner (`project-1-migration`)

Before/after suites for mechanical, every-file-touched migrations.

```sh
cd project-1-migration/python-sample
uv venv && source .venv/bin/activate && uv pip install pytest
python -m unittest discover -s tests -p 'test_legacy_unittest.py' -t .  # legacy: 12 pass
python -m pytest tests/test_migrated_pytest.py -v                       # migrated: 15 pass
python3 check_parity.py                                                 # 10 parity checks

cd ../js-sample
node test/test-legacy.cjs                   # legacy: 12 asserts
node --test test/test-migrated.test.mjs     # migrated: 13 pass
```

## 2 — Cold-start feature (`project-2-coldstart`)

A layered task tracker (store → service → CLI + docs). The agent was handed
only `TASK.md` and implemented tags across all layers. Try it:

```sh
cd project-2-coldstart/python
uv venv && source .venv/bin/activate && uv pip install pytest
python -m pytest tests/ -q                  # 10 passed
python -m tasks.cli add "Write report" --tags work,urgent
python -m tasks.cli list --tag work

cd ../js
node --test test/tags.test.mjs              # 10 passed
node src/cli.mjs add "Write report" --tags=work,urgent
node src/cli.mjs list --tag=work
```

## 3 — Test-and-fix swarm (`project-3-test-swarm`)

A billing module with a deliberately thin suite, plus the expanded full suite.

```sh
cd project-3-test-swarm/python
uv venv && source .venv/bin/activate && uv pip install pytest
python -m unittest tests.test_weak -v       # before: 2 tests
python -m pytest tests/test_full.py -q      # after: 23 passed

cd ../js
node test/test-weak.mjs                     # before: 2 checks
node --test test/test-full.test.mjs         # after: 23 passed
```

## 4 — Polyglot CLI (`project-4-polyglot`)

Scaffold minimal tested projects in TypeScript, Go, or Rust:

```sh
cd project-4-polyglot
uv venv && source .venv/bin/activate && uv pip install pytest
python -m pytest tests/ -q                  # 12 passed
python cli/scaffold.py --lang ts --name demo --out /tmp/out
python cli/scaffold.py --lang go --name demo --out /tmp/out
python cli/scaffold.py --lang rust --name demo --out /tmp/out
sh e2e/check.sh                             # E2E OK (runs real cargo + node checks when present)
```

## 5 — Docs-to-code (`project-5-docs-to-code`)

Edit the spec, regenerate, test — the full loop in seconds:

```sh
cd project-5-docs-to-code
uv venv && source .venv/bin/activate && uv pip install pytest
python gen/generate.py                      # spec/openapi.json -> out/server.py, out/client.py, out/mocks.py
python -m pytest tests/ -q                  # 10 passed
```

`out/` is committed; CI regenerates and fails on drift.

## 6 — Bug-hunt marathon (`project-6-bughunt`)

Ten injected bugs (5 Python + 5 JS) with repro scripts, proof logs, a hunter
log template (`BUGLOG.md`), and documented fixes (`SOLUTIONS.md`).

```sh
cd project-6-bughunt/python
uv venv && source .venv/bin/activate && uv pip install pytest
python repro/repro.py                       # 5/5 passed
python -m pytest tests/ -q                  # 7 passed

cd ../js
node repro/repro.mjs                        # 5/5 passed
node --test test/regress.test.mjs           # 5 passed
```

`proof/before-fix.log` files preserve the original 0/5 red runs. To score
another agent: reset the sources to the buggy state described in
`SOLUTIONS.md`, hand it `BUGLOG.md`, and count fixes out of 10.

## 7 — Self-healing CI (`heal.sh`, `.github/workflows`, `docker/`)

One command runs everything — all pytest suites, all node suites, the #5
regen drift check, and ruff lint with auto-fix:

```sh
sh heal.sh                                  # HEALED: all green
```

The GitHub workflow mirrors it per-job, plus a Docker build:

```sh
docker build -f docker/Dockerfile -t muse-projects .
```

## 8 — Strict typing (`project-8-strict-typing`)

`before/` is the frozen untyped snapshot; `app/` is the same code under
`mypy --strict` with an ascent log.

```sh
cd project-8-strict-typing
uv venv && source .venv/bin/activate && uv pip install pytest mypy
python -m pytest tests/ -q                  # 10 passed
python -m mypy app                          # no issues found
```

## 9 — Traffic-to-SDK (`project-9-traffic-sdk`)

```sh
cd project-9-traffic-sdk
uv venv && source .venv/bin/activate && uv pip install pytest
python gen/build_sdk.py                     # 5 endpoints inferred
python -m pytest tests/ -q                  # 10 passed
```

## 10 — Upgrade cascade (`project-10-upgrade`)

```sh
cd project-10-upgrade
uv venv && source .venv/bin/activate && uv pip install pytest
python -m pytest tests/ -q                  # 8 passed
```

Breakage order in `UPGRADE.md`: billing rename, notify kwarg, CLI free.

## 11 — Log-to-dashboard (`project-11-log-dashboard`)

```sh
cd project-11-log-dashboard
uv venv && source .venv/bin/activate && uv pip install pytest
python gen_logs.py && python analyze.py     # report.db + report.html
python -m pytest tests/ -q                  # 8 passed
```

## 12 — Config drift doctor (`project-12-config-drift`)

```sh
cd project-12-config-drift
uv venv && source .venv/bin/activate && uv pip install pytest
python doctor.py                            # 6 findings
python -m pytest tests/ -q                  # 8 passed
```

## 13 — Dead-code census (`project-13-deadcode`)

```sh
cd project-13-deadcode
uv venv && source .venv/bin/activate && uv pip install pytest
python census.py src                        # 0 dead symbols
python -m pytest tests/ -q                  # 8 passed
```

## 14 — Fuzz farmer (`project-14-fuzz`)

```sh
cd project-14-fuzz
uv venv && source .venv/bin/activate && uv pip install pytest
python fuzz.py 5000                         # 5000/5000 ok (red run in findings.log)
python -m pytest tests/ -q                  # 10 passed
```

## 15 — i18n (`project-15-i18n`)

```sh
cd project-15-i18n
uv venv && source .venv/bin/activate && uv pip install pytest
python tools/check.py                       # missing=0
python -m pytest tests/ -q                  # 8 passed
```

## 16 — Migration rehearsal (`project-16-rehearsal`)

```sh
cd project-16-rehearsal
uv venv && source .venv/bin/activate && uv pip install pytest
python rehearse.py                          # REHEARSAL OK, byte-identical
python -m pytest tests/ -q                  # 8 passed
```

## 17 — Perf tracker (`project-17-perf`)

```sh
cd project-17-perf
uv venv && source .venv/bin/activate && uv pip install pytest
python bench.py && python gate.py && python trend.py   # GATE OK
python -m pytest tests/ -q                  # 8 passed
```
