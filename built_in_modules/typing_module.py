# -*- coding: utf-8 -*-
# @Time    : 2019-06-17 10:46
# @Author  : Woko
# @File    : typing_module.py

"""typing
这次只为写一个有趣的功能，typing.overload
谨记：这并不是真正的重载，只是 type hints
用法如下：
1. 先标记几种输入和输出类型
2. 真正实现这个函数，这时的输入和输出不需要再指定类型了

对于"多种输入类型，多种输出类型"，
静态类型检测时，会按照标记的类型进行对应检测
在 pycharm 里写代码时，也会给出相应提示
"""

from typing import overload


@overload
def build_a_house(height: None) -> None: ...
@overload
def build_a_house(height: int) -> str: ...
@overload
def build_a_house(height: int, name: str) -> str: ...


def build_a_house(height, name=None):
    if height is None:
        return None
    elif isinstance(height, int):
        message = 'building a house with %d height' % height
    elif isinstance(height, float):
        message = 'building a house with %f height' % height
    else:
        raise TypeError('height must be int or float')
    if name:
        message += ' and named with %s' % name
    return message


print(build_a_house(None))
print(build_a_house(4))
print(build_a_house(4, 'Link\'s Home'))
