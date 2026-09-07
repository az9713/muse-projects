# Task Tracker — API notes

Layers: `tasks/store.py` (JSON-file persistence) -> `tasks/service.py`
(validation + rules) -> `tasks/cli.py` (`add` / `list` / `done`).

## Tasks

- `id`: auto-increment int
- `title`: non-empty string
- `done`: bool, default false
- `tags`: list of lowercase slugs, default `[]`, stored sorted, deduped

## Service rules

- Titles are stripped; empty titles raise `ValueError`.
- Tags are stripped, lowercased, deduped; empty tags raise `ValueError`.
- `list_tasks(tag=...)` filters to tasks carrying the tag (case-insensitive).
- `open_tasks(tag=...)` combines the tag filter with `done == False`.

## CLI

```sh
python -m tasks.cli add "Write report" --tags work,urgent
python -m tasks.cli list --tag work
python -m tasks.cli list --tag work --open
python -m tasks.cli done 1
```
