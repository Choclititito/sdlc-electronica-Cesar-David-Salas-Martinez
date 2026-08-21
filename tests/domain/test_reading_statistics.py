"""tests/domain/test_reading_statistics.py
TDD: escrito antes de app.domain.reading_statistics.
"""
import pytest
from app.domain.reading_statistics import compute_statistics, ReadingStatistics


def test_empty_list_returns_none_stats():
    stats = compute_statistics([])
    assert stats == ReadingStatistics(count=0, minimum=None, maximum=None, average=None)


def test_single_value_returns_that_value_for_all_stats():
    stats = compute_statistics([25.0])
    assert stats.count == 1
    assert stats.minimum == 25.0
    assert stats.maximum == 25.0
    assert stats.average == 25.0


def test_multiple_values_computes_correct_stats():
    stats = compute_statistics([10.0, 20.0, 30.0])
    assert stats.count == 3
    assert stats.minimum == 10.0
    assert stats.maximum == 30.0
    assert stats.average == 20.0


def test_average_rounds_to_two_decimals():
    stats = compute_statistics([1.0, 2.0, 2.0])
    # promedio real = 1.6666...
    assert stats.average == 1.67


def test_negative_values_are_handled_correctly():
    stats = compute_statistics([-10.0, 0.0, 10.0])
    assert stats.minimum == -10.0
    assert stats.maximum == 10.0
    assert stats.average == 0.0


def test_all_identical_values():
    stats = compute_statistics([5.0, 5.0, 5.0])
    assert stats.minimum == stats.maximum == stats.average == 5.0