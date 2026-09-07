"""Service layer: validation + business rules over the store."""
from tasks import store


def _clean_tags(tags):
    cleaned = []
    for tag in tags or []:
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("tags must be non-empty strings")
        if tag not in cleaned:
            cleaned.append(tag)
    return cleaned


def create_task(title, tags=(), db_path=None):
    title = title.strip()
    if not title:
        raise ValueError("title must be non-empty")
    kw = {"db_path": db_path} if db_path else {}
    return store.add_task(title, _clean_tags(tags), **kw)


def list_tasks(tag=None, db_path=None):
    kw = {"db_path": db_path} if db_path else {}
    if tag is not None:
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("tag filter must be non-empty")
    return store.list_tasks(tag=tag, **kw)


def complete_task(task_id, db_path=None):
    kw = {"db_path": db_path} if db_path else {}
    return store.set_done(task_id, True, **kw)


def open_tasks(tag=None, db_path=None):
    return [t for t in list_tasks(tag=tag, db_path=db_path) if not t["done"]]
