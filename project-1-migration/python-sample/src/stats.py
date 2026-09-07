"""Stats helpers (migration sample)."""


def mean(values):
    if not values:
        raise ValueError("empty")
    return sum(values) / len(values)


def clamp(value, low, high):
    return max(low, min(high, value))


def pct_change(old, new):
    if old == 0:
        raise ValueError("old must be non-zero")
    return (new - old) / old * 100.0
