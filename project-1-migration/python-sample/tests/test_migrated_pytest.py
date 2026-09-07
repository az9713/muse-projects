"""MIGRATED suite: pytest style (after migration). Target run: python -m pytest tests/test_migrated_pytest.py -v
Runs under pytest once installed (pip install pytest). Mirrors the legacy suite
with plain asserts, fixtures and parametrize — no TestCase boilerplate.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from calc import add, div, mul, sub
from stats import clamp, mean, pct_change
from strings import count_words, slugify, truncate


@pytest.fixture()
def sample_values():
    return [1, 2, 3, 4]


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(2, 3, 5), (-1, 1, 0), (0, 0, 0)],
)
def test_add(a, b, expected):
    assert add(a, b) == expected


def test_sub():
    assert sub(5, 3) == 2


def test_mul():
    assert mul(3, 4) == 12


def test_div():
    assert div(7, 2) == pytest.approx(3.5)


def test_div_zero():
    with pytest.raises(ValueError):
        div(1, 0)


def test_slugify():
    assert slugify("Hello World") == "hello-world"


def test_truncate_short():
    assert truncate("abc", 10) == "abc"


def test_truncate_long():
    assert truncate("x" * 30, 20).endswith("...")


def test_count_words():
    assert count_words("a b c") == 3


def test_mean(sample_values):
    assert mean(sample_values) == pytest.approx(2.5)


def test_mean_empty():
    with pytest.raises(ValueError):
        mean([])


def test_clamp():
    assert clamp(10, 0, 5) == 5
    assert clamp(-1, 0, 5) == 0


def test_pct_change():
    assert pct_change(100, 120) == pytest.approx(20.0)
