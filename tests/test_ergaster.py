import pytest

from ergaster import add

data = (
    (1, 2, 3),
    (2, 2, 4),
    (3, 2, 5),
)


@pytest.mark.parametrize("x, y, res", data)
def test_add(x, y, res):
    assert add(x, y) == res
