"""Minimal locale runtime with English fallback and {var} interpolation."""
import json
import os

LOCALE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale")
FALLBACK = "en"
_cache = {}


def load(locale):
    if locale not in _cache:
        path = os.path.join(LOCALE_DIR, f"{locale}.json")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                _cache[locale] = json.load(fh)
        else:
            _cache[locale] = {}
    return _cache[locale]


def t(key, locale="en", **variables):
    template = load(locale).get(key, load(FALLBACK).get(key, key))
    try:
        return template.format(**variables)
    except KeyError:
        return template
