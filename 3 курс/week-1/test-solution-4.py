import pytest
import math
solution4 = __import__('solution-4')
factorial = solution4.factorial


def test_basic_cases():
    assert factorial(5) == 120
    assert factorial(0) == 1
    r = range(100)
    assert [factorial(i) for i in r] == [math.factorial(i) for i in r]


def test_type_error_cases():
    with pytest.raises(ValueError) as excinfo:
        factorial('2')
    assert str(excinfo.value) == 'Argument n must be an integer'

    with pytest.raises(ValueError) as excinfo:
        factorial([3])
    assert str(excinfo.value) == 'Argument n must be an integer'

    with pytest.raises(ValueError) as excinfo:
        factorial(tuple([3]))
    assert str(excinfo.value) == 'Argument n must be an integer'


def test_sign_error_cases():
    with pytest.raises(ValueError) as excinfo:
        factorial(-1)
    assert str(excinfo.value) == 'Argument n must be non-negative'
