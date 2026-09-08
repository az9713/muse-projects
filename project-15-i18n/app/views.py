"""Views: all user-facing strings go through t() — no hardcoded UI text."""
from app.i18n import t


def greeting(locale, name):
    return t("hello", locale, name=name)


def farewell(locale, name):
    return t("bye", locale, name=name)


def inbox(locale, count):
    return t("inbox", locale, count=count)
