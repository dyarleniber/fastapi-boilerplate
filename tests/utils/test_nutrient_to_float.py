from fastapi_boilerplate.utils.nutrient_to_float import nutrient_to_float


def test_nutrient_to_float_with_none():
    assert nutrient_to_float(None) == None


def test_nutrient_to_float_with_zero():
    assert nutrient_to_float(0) == None


def test_nutrient_to_float_with_1():
    assert nutrient_to_float(1) == 0.01


def test_nutrient_to_float_with_11():
    assert nutrient_to_float(11) == 0.11


def test_nutrient_to_float_with_100():
    assert nutrient_to_float(100) == 1


def test_nutrient_to_float_with_111():
    assert nutrient_to_float(111) == 1.11


def test_nutrient_to_float_with_116():
    assert nutrient_to_float(116) == 1.16


def test_nutrient_to_float_with_1111():
    assert nutrient_to_float(1111) == 11.11


def test_nutrient_to_float_with_11111():
    assert nutrient_to_float(11111) == 111.11


def test_nutrient_to_float_with_123456789():
    assert nutrient_to_float(123456789) == 1234567.89


def test_nutrient_to_float_with_negative_1():
    assert nutrient_to_float(-1) == None
