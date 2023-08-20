from fastapi_boilerplate.utils.milligrams_to_grams import milligrams_to_grams


def test_milligrams_to_grams_with_none():
    assert milligrams_to_grams(None) == None


def test_milligrams_to_grams_with_zero():
    assert milligrams_to_grams(0) == None


def test_milligrams_to_grams_with_1():
    assert milligrams_to_grams(1) == 0.001


def test_milligrams_to_grams_with_10():
    assert milligrams_to_grams(10) == 0.01


def test_milligrams_to_grams_with_100():
    assert milligrams_to_grams(100) == 0.1


def test_milligrams_to_grams_with_1000():
    assert milligrams_to_grams(1000) == 1


def test_milligrams_to_grams_with_10000():
    assert milligrams_to_grams(10000) == 10


def test_milligrams_to_grams_with_100000():
    assert milligrams_to_grams(100000) == 100


def test_milligrams_to_grams_with_1000000():
    assert milligrams_to_grams(1000000) == 1000


def test_milligrams_to_grams_with_123456789():
    assert milligrams_to_grams(123456789) == 123456.789


def test_milligrams_to_grams_with_123456_789():
    assert milligrams_to_grams(123456.789) == 123.456789


def test_milligrams_to_grams_with_negative_1():
    assert milligrams_to_grams(-1) == None
