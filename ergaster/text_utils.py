_g_qwerty_en_ru_tbl = None


def qwerty_en_ru_tbl_factory():
    en1 = r"""`1234567890-=qwertyuiop[]asdfghjkl;'\zxcvbnm,./"""
    ru1 = r"""ё1234567890-=йцукенгшщзхъфывапролджэ\ячсмитьбю."""
    en2 = r"""~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:"||ZXCVBNM<>?"""
    ru2 = r"""Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ//ЯЧСМИТЬБЮ,"""
    s1 = en1 + en2 + ru1 + ru2
    s2 = ru1 + ru2 + en1 + en2
    tbl = str.maketrans(s1, s2)
    return tbl


def get_qwerty_en_ru_tbl():
    global _g_qwerty_en_ru_tbl
    if _g_qwerty_en_ru_tbl is None:
        _g_qwerty_en_ru_tbl = qwerty_en_ru_tbl_factory()
    return _g_qwerty_en_ru_tbl


def str_qwerty_en_ru(s: str) -> str:
    """
    >>> str_qwerty_en_ru("Еуые")
    Test
    >>> str_qwerty_en_ru("Ghbdtn")
    Привет
    """
    return s.translate(get_qwerty_en_ru_tbl())
