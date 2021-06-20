import sys

sys.path.insert(0, "src")

import pytest

from ergaster.ergaster import add

data = (
    (1, 2, 3),
    (2, 2, 4),
)


@pytest.mark.parametrize("x, y, res", data)
def test_add(x, y, res):
    assert add(x, y) == res
