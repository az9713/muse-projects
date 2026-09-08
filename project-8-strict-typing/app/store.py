"""AFTER: fully strict-typed JSON store (mypy --strict clean)."""
from __future__ import annotations

import json
import os
from dataclasses import asdict

from app.models import Task

DB = os.path.join(os.path.dirname(__file__), "tasks.json")


def load(db_path: str | None = None) -> list[Task]:
    path = db_path or DB
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        rows: list[dict[str, object]] = json.load(fh)
    tasks: list[Task] = []
    for row in rows:
        raw_tags = row.get("tags", [])
        tags = [str(t) for t in raw_tags] if isinstance(raw_tags, list) else []
        tasks.append(
            Task(
                id=int(str(row["id"])),
                title=str(row["title"]),
                done=bool(row.get("done", False)),
                tags=tags,
            )
        )
    return tasks


def save(tasks: list[Task], db_path: str | None = None) -> None:
    path = db_path or DB
    with open(path, "w", encoding="utf-8") as fh:
        json.dump([asdict(t) for t in tasks], fh, indent=2)


def add(task: Task, db_path: str | None = None) -> Task:
    tasks = load(db_path)
    tasks.append(task)
    save(tasks, db_path)
    return task
