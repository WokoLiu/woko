# -*- coding: utf-8 -*-
# @Time    : 2018/7/8 22:47
# @Author  : Woko
# @File    : ordered_default_dict.py

"""创建一个同时满足 defaultdict 和 OrderedDict 的字典
注意，OrderedDict 本身大小就是普通字典的两倍多，使用时注意开销
"""

from collections import defaultdict
from collections import OrderedDict


class OrderedDefaultDict(OrderedDict, defaultdict):
    def __init__(self, default_factory=None, *args, **kwargs):
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory


if __name__ == '__main__':
    a = OrderedDefaultDict(list)
    a['a'].append(1)
    a['b'].append(2)

    b = OrderedDefaultDict(list)
    b['b'].append(2)
    b['a'].append(1)

    print(a)
    print(b)
