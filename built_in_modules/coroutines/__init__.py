# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 14:46
# @Author  : Woko
# @File    : __init__.py.py

"""写着玩的协程例子"""

from typing import Generator, Union, List


def int_to_str() -> Generator[int, str, str]:
    res = ''
    for i in range(10):
        res += yield i
    return res


def str_to_int() -> Generator[str, int, int]:
    res = 0
    for i in range(10):
        res += yield str(i)
    return res


def to_bytes() -> Generator[bytes, Union[str, int], None]:
    while 1:
        value = yield from int_to_str()
        yield bytes(value, encoding='utf8')

        value = yield from str_to_int()
        yield bytes(str(value), encoding='utf8')


def run() -> List[bytes]:
    x = to_bytes()
    item = next(x)
    res = []
    for _ in range(22):
        if isinstance(item, str):
            item = x.send(int(item))
        elif isinstance(item, int):
            item = x.send(str(item))
        else:  # must be bytes
            res.append(item)
            item = next(x)
    return res


if __name__ == '__main__':
    print(run())  # [b'0123456789', b'45']
