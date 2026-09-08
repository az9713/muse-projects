"""BEFORE snapshot: untyped code, the ascent starting point (do not edit)."""


class Task:
    def __init__(self, id, title, done=False, tags=None):
        self.id = id
        self.title = title
        self.done = done
        self.tags = tags or []


def new_task(id, title, tags=None):
    return Task(id, title.strip(), False, tags)


def is_open(task):
    return not task.done
