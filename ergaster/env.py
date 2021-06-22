import datetime
import os
import sys
from typing import Any, Callable, Dict, List, Mapping, Optional

import pyperclip


###################################################################################################################
from ergaster.dot_clip import shorten_to_line


class DictOverride:
    """
    >>> fns = dict(is_windows=_is_windows, now=datetime.datetime.now, cwd=os.getcwd)
    >>> fns = dict(is_windows=lambda: False, now=lambda: datetime.datetime(2021, 1, 2), cwd=lambda: "/home/user")
    >>> overrides = dict(is_windows=True, now=datetime.datetime(2022, 3, 4), cwd='/')
    >>> d = DictOverride(fns, overrides)
    >>> d.avail_keys()
    dict_keys(['is_windows', 'now', 'cwd'])
    >>> d['is_windows']
    True
    >>> d['is_windows'] = None
    >>> d['is_windows']
    False
    >>> d['cwd']
    '/'
    >>> d['cwd'] = None
    >>> d['cwd']
    '/home/user'
    >>> d['non_avail_key']
    Traceback (most recent call last):
    ...
    KeyError: 'non_avail_key'
    >>> d['non_avail_key'] = 123
    Traceback (most recent call last):
    ...
    KeyError: 'non_avail_key'
    """

    def __init__(self, fn_dict: [str, Callable], values: Dict[str, Any]):
        if values is None:
            values = {}
        self.fn_dict = fn_dict
        self.values_dict = values

    def avail_keys(self) -> List[str]:
        return self.fn_dict.keys()

    def is_key_avail(self, key: str) -> bool:
        return key in self.fn_dict

    def __getitem__(self, key: str) -> Any:
        if not self.is_key_avail(key):
            raise KeyError(key)
        val = self.values_dict.get(key)
        if val is None:
            val = self.fn_dict[key]()
        return val

    def __setitem__(self, key: str, value: Any):
        if not self.is_key_avail(key):
            raise KeyError(key)
        if value is None:
            del self.values_dict[key]
        else:
            self.values_dict[key] = value

    def from_dict(self, d: Mapping[str, Any]) -> None:
        for k, v in d.items():
            self[k] = v

    def as_dict(self) -> Mapping[str, Any]:
        return {(k, self[k]) for k in self.fn_dict}


#######################################################################################################################
def _is_windows():
    return os.name == "nt"


def _get_stdout():
    return sys.stdout


def _get_stderr():
    return sys.stderr


def get_default_clip():
    return ClipPyperclip()


def is_file_obj(x):
    return hasattr(x, "id")


def str_println(*args: Any) -> str:
    r"""
    >>> str_println(1, 2, 3)
    '1 2 3\n'
    """
    return " ".join(map(str, args)) + "\n"


def file_println(file_obj, *args: Any):
    sep = ""
    for x in args:
        file_obj.write(sep)
        file_obj.write(str(x))
        sep = " "
    file_obj.write("\n")


class StrFile:
    def __init__(self):
        self.buf = ""

    def write(self, s: str):
        self.buf += s


class ClipPyperclip:
    # @staticmethod
    def copy_bytes(bts: bytes) -> None:
        pyperclip.copy(bts)

    # @staticmethod
    def paste_bytes() -> bytes:
        return pyperclip.paste()


class ClipMonk:
    def __init__(self):
        self.buf = b""

    def copy_bytes(self, bts: bytes) -> None:
        self.buf = bts

    def paste_bytes(self) -> bytes:
        return self.buf


class Env:
    r"""
    >>> env = Env(is_windows=False, cwd='/root', now=datetime.datetime(2021, 6, 1))
    >>> env.overrides_as_dict() == {'is_windows': False, 'cwd': '/root', 'now': datetime.datetime(2021, 6, 1, 0, 0)}
    True
    >>> env.is_windows()
    False
    >>> env.cwd()
    '/root'
    >>> env.now()
    datetime.datetime(2021, 6, 1, 0, 0)
    >>> env.println(1, 2, 3)
    1 2 3
    >>> out = StrFile()
    >>> env.set_stdout(out)
    >>> env.println(4, 5, 6)
    >>> out.buf
    '4 5 6\n'
    >>> err = StrFile()
    >>> env.set_stderr(err)
    >>> env.eprintln("error", "message")
    >>> err.buf
    'error message\n'
    >>> out = StrFile()
    >>> env.set_stdout(out)
    >>> env.set_stderr(out)
    >>> env.println("std", "message")
    >>> env.eprintln("error", "message")
    >>> out.buf
    'std message\nerror message\n'
    >>> clip = ClipMonk
    >>> env = Env(clip=clip)
    >>> env.clip_copy('text to clip')
    """

    # env.is_windows() == False
    # Falsee
    # env.cwd()
    # Falsee
    def __init__(self, **kwargs):
        fns = dict(
            is_windows=_is_windows,
            now=datetime.datetime.now,
            cwd=os.getcwd,
            stdout=_get_stdout,
            stderr=_get_stderr,
            # clip=ClipPyperclip,
            clip=get_default_clip,
        )
        self.overrides = DictOverride(fns, kwargs)

    ###################################################################################################################
    def println(self, *args):
        file_println(self.stdout(), *args)

    def eprintln(self, *args):
        file_println(self.stderr(), *args)

    def clip_copy(self, s):
        self.println("clipboard <<<", shorten_to_line(s))
        bts = bytes(s, 'utf8')
        self.clip().copy_bytes(bts)

    def clip_paste(self, s):
        return self.clip().paste_bytes()

    ###################################################################################################################
    # def __getitem__(self, key: str) -> Any:
    #     return self.overrides[key]
    #
    # def __setitem__(self, key: str, value: Any) -> None:
    #     self.overrides[key] = value

    ###################################################################################################################
    def from_dict(self, d: Mapping[str, Any]):
        self.overrides.from_dict(d)

    def as_dict(self):
        return self.overrides.as_dict()

    def overrides_as_dict(self):
        return self.overrides.values_dict

    ###################################################################################################################
    def stdout(self):
        return self.overrides["stdout"]

    def set_stdout(self, val):
        self.overrides["stdout"] = val

    def stderr(self):
        return self.overrides["stderr"]

    def set_stderr(self, val):
        self.overrides["stderr"] = val

    def clip(self):
        return self.overrides["clip"]

    def set_clip(self, val):
        self.overrides["clip"] = val

    ###################################################################################################################
    def is_windows(self):
        return self.overrides["is_windows"]

    def set_is_windows(self, val):
        self.overrides["is_windows"] = val

    def now(self):
        return self.overrides["now"]

    def set_now(self, val):
        self.overrides["now"] = val

    def cwd(self):
        return self.overrides["cwd"]

    def set_cwd(self, val):
        self.overrides["cwd"] = val

    ###################################################################################################################
    def now_formatted(self, dt_format: str) -> str:
        return self.now().strftime(dt_format)


#######################################################################################################################
_g_env = None


def global_env():
    global _g_env
    if _g_env is None:
        _g_env = Env()
    return _g_env


###################################################################################################################
def _main():
    def print_env(e):
        print(e.overrides_as_dict())
        print(e.as_dict())
        print("-----")

    env = global_env()
    print_env(env)
    env.from_dict(dict(cwd="/"))
    print_env(env)
    env.set_is_windows(True)
    print_env(env)
    env.set_is_windows(None)
    print_env(env)


def env_doctests():
    import doctest

    doctest.testmod()


###################################################################################################################
if __name__ == "__main__":
    # _main()
    env_doctests()
