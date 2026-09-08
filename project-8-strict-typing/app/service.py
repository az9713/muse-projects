"""AFTER: fully strict-typed service layer (mypy --strict clean)."""
from __future__ import annotations

from app.models import Task, is_open, new_task
from app.store import add, load, save


def create(title: str, tags: list[str] | None = None, db_path: str | None = None) -> Task:
    tasks = load(db_path)
    task = new_task(max([t.id for t in tasks], default=0) + 1, title, tags)
    return add(task, db_path)


def open_tasks(db_path: str | None = None) -> list[Task]:
    return [t for t in load(db_path) if is_open(t)]


def complete(task_id: int, db_path: str | None = None) -> Task:
    tasks = load(db_path)
    for task in tasks:
        if task.id == task_id:
            task.done = True
            save(tasks, db_path)
            return task
    raise KeyError(f"no task {task_id}")
