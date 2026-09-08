"""Vendor lib v2 (current) — two breaking changes vs v1 (see UPGRADE.md).

1. format_amount(cents) -> format_money(amount_cents, currency="USD")
2. send(to, msg) now requires keyword-only channel=
"""
from __future__ import annotations


def format_money(amount_cents: int, currency: str = "USD") -> str:
    symbols = {"USD": "$", "EUR": "\u20ac", "GBP": "\u00a3"}
    return f"{symbols.get(currency, currency + ' ')}{amount_cents / 100:.2f}"


def send(to: str, msg: str, *, channel: str) -> dict[str, object]:
    if channel not in ("email", "sms"):
        raise ValueError(f"unknown channel: {channel}")
    return {"to": to, "msg": msg, "channel": channel, "sent": True}
