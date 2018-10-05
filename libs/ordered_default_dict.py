# -*- coding: utf-8 -*-
# @Time    : 2018/7/8 22:47
# @Author  : Woko
# @File    : ordered_default_dict.py

"""创建一个同时满足 defaultdict 和 OrderedDict 的字典
注意，OrderedDict 本身大小就是普通字典的两倍多，使用时注意开销
note: after python 3.6 'dict keeps insertion order'.
see: https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6
"""

import sys
from collections import defaultdict
from collections import OrderedDict

if sys.version_info[0] < 3:
    class OrderedDefaultDict(OrderedDict, defaultdict):
        def __init__(self, default_factory=None, *args, **kwargs):
            super(OrderedDefaultDict, self).__init__(*args, **kwargs)
            self.default_factory = default_factory
else:
    class OrderedDefaultDict(OrderedDict):
        def __init__(self, default_factory=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.default_factory = default_factory

        def __getitem__(self, item):
            if item in self:
                return super().__getitem__(item)
            else:
                return self.setdefault(item, self.default_factory())

