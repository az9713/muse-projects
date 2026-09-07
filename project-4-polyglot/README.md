# #4 Polyglot CLI toolchain

One Python CLI scaffolds minimal runnable projects in three languages:

```sh
cd cli
python3 scaffold.py --lang ts --name demo --out /tmp/out
python3 scaffold.py --lang go --name demo --out /tmp/out
python3 scaffold.py --lang rust --name demo --out /tmp/out
```

Each scaffold ships with a working test (`node --test` / `go test` /
`cargo test`). Toolchains are NOT required here — only Python 3.

## Verify (project env)

```sh
source .venv/bin/activate
python -m pytest tests/ -q     # 12 passed
sh e2e/check.sh                # scaffold + content + opportunistic toolchain checks
```

`e2e/check.sh` runs the real `tsc`/`go`/`cargo` checks only when those
binaries exist; otherwise it verifies structure + content and skips loudly.
