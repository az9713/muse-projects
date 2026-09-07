# Task Tracker — API notes

Layers: `src/store.mjs` (JSON-file persistence) -> `src/service.mjs`
(validation + rules) -> `src/cli.mjs` (`add` / `list` / `done`).

## Tasks

- `id`: auto-increment int
- `title`: non-empty string
- `done`: bool, default false
- `tags`: list of lowercase slugs, default `[]`, stored sorted, deduped

## Service rules

- Titles are stripped; empty titles throw.
- Tags are stripped, lowercased, deduped; empty tags throw.
- `listTasks(tag)` filters to tasks carrying the tag (case-insensitive).
- `openTasks(tag)` combines the tag filter with `done === false`.

## CLI

```sh
node src/cli.mjs add "Write report" --tags=work,urgent
node src/cli.mjs list --tag=work
node src/cli.mjs list --tag=work --open
node src/cli.mjs done 1
```
