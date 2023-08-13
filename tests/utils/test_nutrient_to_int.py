from fastapi_boilerplate.utils.nutrient_to_int import nutrient_to_int


def test_nutrient_to_int_with_none():
    assert nutrient_to_int(None) == None


def test_nutrient_to_int_with_zero():
    assert nutrient_to_int(0) == None


def test_nutrient_to_int_with_0_1():
    assert nutrient_to_int(0.1) == 10


def test_nutrient_to_int_with_0_11():
    assert nutrient_to_int(0.11) == 11


def test_nutrient_to_int_with_0_111():
    assert nutrient_to_int(0.111) == 11


def test_nutrient_to_int_with_0_116():
    assert nutrient_to_int(0.116) == 12


def test_nutrient_to_int_with_0_001():
    assert nutrient_to_int(0.001) == 0


def test_nutrient_to_int_with_0_006():
    assert nutrient_to_int(0.006) == 1


def test_nutrient_to_int_with_1():
    assert nutrient_to_int(1) == 100


def test_nutrient_to_int_with_11_11():
    assert nutrient_to_int(11.11) == 1111


def test_nutrient_to_int_with_111_111():
    assert nutrient_to_int(111.111) == 11111


def test_nutrient_to_int_with_1111_116():
    assert nutrient_to_int(1111.116) == 111111


def test_nutrient_to_int_with_123456_789():
    assert nutrient_to_int(123456.789) == 12345679


def test_nutrient_to_int_with_negative_1():
    assert nutrient_to_int(-1) == None
