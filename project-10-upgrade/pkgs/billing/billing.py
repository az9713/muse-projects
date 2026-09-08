"""Billing package (migrated to lib v2)."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "vendor"))

from lib import format_money


def invoice_total(items_cents: list[int], currency: str = "USD") -> str:
    return format_money(sum(items_cents), currency)
