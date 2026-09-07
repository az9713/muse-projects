"""Order totals (5 injected bugs B1..B5, all fixed — see SOLUTIONS.md)."""
from datetime import datetime

CATALOG = {
    "widget": {"price": 10.00, "cost": 6.00},
    "gadget": {"price": 25.50, "cost": 15.00},
}

PROMO_EXPIRY = "12/31/2026"  # non-ISO format


def bulk_rate(qty):
    if qty >= 100:
        return 0.20
    if qty >= 50:
        return 0.10
    return 0.0


def add_note(note, notes=None):
    notes = list(notes) if notes else []
    notes.append(note)
    return notes


def line_total(price, qty):
    return round(price * qty + 1e-9, 2)


def _parse(date_str):
    return datetime.strptime(date_str, "%m/%d/%Y").date()


def promo_active(today=None):
    today = _parse(today) if today else datetime.now().date()
    return today <= _parse(PROMO_EXPIRY)


def receipt(sku, qty):
    item = CATALOG[sku]
    subtotal = line_total(item["price"], qty)
    total = round(subtotal * (1 - bulk_rate(qty)), 2)
    out = {"sku": sku, "qty": qty, "total": total}
    return out
