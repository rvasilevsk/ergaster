import pytest

from ergaster.text_utils import str_qwerty_en_ru


#######################################################################################################################
data = (
    ("", ""),
    ("Еуые", "Test"),
    ("Ghbdtn", "Привет"),
    ("123", "123"),
)


@pytest.mark.parametrize("s1, s2", data)
def test_str_qwerty_en_ru(s1, s2):
    assert str_qwerty_en_ru(s1) == s2
