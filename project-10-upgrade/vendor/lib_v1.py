"""BEFORE: vendor lib v1 (frozen) — callers in pkgs/ used this API."""


def format_amount(cents):
    return f"${cents / 100:.2f}"


def send(to, msg):
    return {"to": to, "msg": msg, "sent": True}
