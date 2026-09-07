"""Billing helpers (test-swarm target). Intentionally small but branchy."""


def line_total(price, qty):
    if qty < 0:
        raise ValueError("qty must be >= 0")
    if price < 0:
        raise ValueError("price must be >= 0")
    return round(price * qty, 2)


def discount_rate(qty):
    if qty >= 100:
        return 0.20
    if qty >= 50:
        return 0.10
    if qty >= 10:
        return 0.05
    return 0.0


def apply_discount(total, qty):
    return round(total * (1 - discount_rate(qty)), 2)


def with_tax(total, rate=0.07):
    if rate < 0:
        raise ValueError("rate must be >= 0")
    return round(total * (1 + rate), 2)


def invoice(price, qty, rate=0.07):
    subtotal = line_total(price, qty)
    discounted = apply_discount(subtotal, qty)
    return {
        "subtotal": subtotal,
        "discount": round(subtotal - discounted, 2),
        "total": with_tax(discounted, rate),
    }
