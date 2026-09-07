"""Data layer: JSON-file backed task store. Tasks have id, title, done, tags."""
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "tasks.json")


def _load(db_path=DB_PATH):
    if not os.path.exists(db_path):
        return []
    with open(db_path, encoding="utf-8") as fh:
        return json.load(fh)


def _save(rows, db_path=DB_PATH):
    with open(db_path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2)


def add_task(title, tags=(), db_path=DB_PATH):
    rows = _load(db_path)
    task = {
        "id": max([r["id"] for r in rows], default=0) + 1,
        "title": title,
        "done": False,
        "tags": sorted(set(tags)),
    }
    rows.append(task)
    _save(rows, db_path)
    return task


def list_tasks(tag=None, db_path=DB_PATH):
    rows = _load(db_path)
    if tag is None:
        return rows
    return [r for r in rows if tag in r.get("tags", [])]


def get_task(task_id, db_path=DB_PATH):
    for row in _load(db_path):
        if row["id"] == task_id:
            return row
    raise KeyError(f"no task {task_id}")


def set_done(task_id, done=True, db_path=DB_PATH):
    rows = _load(db_path)
    for row in rows:
        if row["id"] == task_id:
            row["done"] = done
            _save(rows, db_path)
            return row
    raise KeyError(f"no task {task_id}")
