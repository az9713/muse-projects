"""BEFORE snapshot: untyped code, the ascent starting point (do not edit)."""
import json
import os

from models import Task

DB = os.path.join(os.path.dirname(__file__), "tasks.json")


def load(db_path=None):
    db_path = db_path or DB
    if not os.path.exists(db_path):
        return []
    with open(db_path) as fh:
        return [Task(**row) for row in json.load(fh)]


def save(tasks, db_path=None):
    db_path = db_path or DB
    with open(db_path, "w") as fh:
        json.dump([t.__dict__ for t in tasks], fh)


def add(task, db_path=None):
    tasks = load(db_path)
    tasks.append(task)
    save(tasks, db_path)
    return task
