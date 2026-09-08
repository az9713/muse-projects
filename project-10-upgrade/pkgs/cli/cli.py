"""CLI package: wires billing + notify (migrated to lib v2)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "billing"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "notify"))

from billing import invoice_total
from notify import receipt


def checkout(to: str, items_cents: list[int]) -> dict[str, object]:
    return receipt(to, invoice_total(items_cents))
