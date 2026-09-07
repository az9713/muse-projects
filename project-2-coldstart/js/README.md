# #2 Cold-start feature — JS task tracker

Mirrors the Python sample: store -> service -> CLI, docs in `docs/API.md`.
The agent was handed only `TASK.md` and implemented tags across all layers.

## Verify

```sh
cd js
node --test test/tags.test.mjs
```

Acceptance: `test/tags.test.mjs`, 10 tests.
