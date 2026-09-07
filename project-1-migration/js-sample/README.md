# #1 Migration runner — JS sample (CommonJS -> ESM)

Dependency-free stand-in for a Jest->Vitest migration: same mechanical
shape (every file touched, imports rewritten, tests re-run), but verifies
with the Node stdlib so no `npm install` is needed.

Legacy: `src/*.cjs` + `test/test-legacy.cjs` (require + asserts).
Migrated: `src/*.mjs` + `test/test-migrated.test.mjs` (import + node:test).

## Verify

```sh
cd js-sample
node test/test-legacy.cjs
node --test test/test-migrated.test.mjs
```

Target upgrade path once deps are available: replace `node:test` with
`vitest` (`npm i -D vitest`, `npx vitest run`).
