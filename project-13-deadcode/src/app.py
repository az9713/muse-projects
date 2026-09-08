"""Live app code (post-census: only reachable symbols remain)."""
from src.models import User
from src.utils import shout


def greet(name):
    user = User(name)
    return shout(f"hello, {user.name}")


def count_admins(users):
    return sum(1 for u in users if u.admin)
