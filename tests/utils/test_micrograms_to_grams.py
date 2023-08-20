from pytest import approx

from fastapi_boilerplate.utils.micrograms_to_grams import micrograms_to_grams


def test_micrograms_to_grams_with_none():
    assert micrograms_to_grams(None) == None


def test_micrograms_to_grams_with_zero():
    assert micrograms_to_grams(0) == None


def test_micrograms_to_grams_with_1000():
    assert micrograms_to_grams(1000) == 0.001


def test_micrograms_to_grams_with_10000():
    assert micrograms_to_grams(10000) == 0.01


def test_micrograms_to_grams_with_100000():
    assert micrograms_to_grams(100000) == 0.1


def test_micrograms_to_grams_with_1000000():
    assert micrograms_to_grams(1000000) == 1


def test_micrograms_to_grams_with_10000000():
    assert micrograms_to_grams(10000000) == 10


def test_micrograms_to_grams_with_100000000():
    assert micrograms_to_grams(100000000) == 100


def test_micrograms_to_grams_with_1000000000():
    assert micrograms_to_grams(1000000000) == 1000


def test_micrograms_to_grams_with_123456789():
    assert micrograms_to_grams(123456789) == approx(123.456789)


def test_micrograms_to_grams_with_123456_789():
    assert micrograms_to_grams(123456.789) == approx(0.123456789)


def test_micrograms_to_grams_with_negative_1():
    assert micrograms_to_grams(-1) == None
