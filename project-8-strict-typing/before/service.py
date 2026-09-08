"""BEFORE snapshot: untyped code, the ascent starting point (do not edit)."""
from models import is_open, new_task
from store import add, load


def create(title, tags=None, db_path=None):
    tasks = load(db_path)
    task = new_task(max([t.id for t in tasks], default=0) + 1, title, tags)
    return add(task, db_path)


def open_tasks(db_path=None):
    return [t for t in load(db_path) if is_open(t)]
