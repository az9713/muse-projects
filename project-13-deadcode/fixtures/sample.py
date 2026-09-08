"""Fixture WITH planted dead code (census must find exactly 3 items)."""
from helpers import used_fn


def live_entry():
    return used_fn()


def orphan_function():
    return "nobody calls me"


class OrphanClass:
    pass
