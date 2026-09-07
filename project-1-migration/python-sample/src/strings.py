"""String helpers (migration sample)."""


def slugify(text):
    return "-".join(text.strip().lower().split())


def truncate(text, limit=20):
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


def count_words(text):
    return len(text.split())
