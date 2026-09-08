"""AFTER: fully strict-typed task model (mypy --strict clean)."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)


def new_task(id: int, title: str, tags: list[str] | None = None) -> Task:
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("title must be non-empty")
    normalized = sorted({t.strip().lower() for t in tags or []})
    if any(not t for t in normalized):
        raise ValueError("tags must be non-empty strings")
    return Task(id, cleaned, False, normalized)


def is_open(task: Task) -> bool:
    return not task.done
