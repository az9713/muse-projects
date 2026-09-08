"""Notify package (migrated to lib v2)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))

from lib import send


def receipt(to: str, total: str) -> dict[str, object]:
    return send(to, f"Your total is {total}", channel="email")
