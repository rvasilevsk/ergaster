import datetime
from typing import Sequence, Union

from pyperclip import paste

from ergaster import env


def erg():
    print(paste())


# if inner_cmd == "paste":
# if inner_cmd == "copy_args":
# if inner_cmd == "copy_stdin":
# if inner_cmd == "copy_cd":
# if inner_cmd == "copy_real_path":
#         return RunUsage("copy_real_path: no arguments")
# if inner_cmd == "copy_ddd":
# if inner_cmd == "copy_mmm":


def copy_ddd(
    args: Sequence[str], now: Union[datetime.date, datetime.datetime, None] = None
):
    """
    >>> copy_ddd(['1', '2', '3'])
    usage
    >>> copy_ddd([], datetime.date(2021, 1, 2))
    clipboard <<< 2021.01.02
    """
    if len(args):
        print("usage")
        return
    if now is None:
        now = env.now()
    s = now.strftime("%Y.%m.%d")
    env.clip_copy(s)


if __name__ == "__main__":
    # copy_ddd([])
    import doctest

    doctest.testmod()
