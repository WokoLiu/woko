# -*- coding: utf-8 -*-
# @Time    : 2017/6/5 18:13
# @Author  : Woko
# @File    : dot_dict.py

"""
使用点操作符，像访问属性一样访问dict的值
当前有两种实现：
1. DocDict，比较简单粗暴，因为dict没有__dict__属性，就把self直接赋给self.__dict__，但是pylint会报E1101
2. ObjectDict，使用__getattr__为点操作符兜底，并且可以连续使用点操作符

"""

__all__ = ['DotDict', 'ObjectDict']


class DotDict(dict):
    """
    使用点操作符访问dict
    """
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class ObjectDict(dict):
    def __getattr__(self, name):
        value = self[name]
        # 下面两行可以保证连续点操作符的使用
        if isinstance(value, dict):
            value = ObjectDict(value)
        return value

if __name__ == '__main__':
    old = {
        'a': 1,
        'b': 2,
        'c': 3,
        'e': {
            'e_1': '想不到吧',
            'e_2': '这样也行'
        }
    }
    try:
        print(old.__dict__)
    except AttributeError as e:
        print(e.args)
        print('dict类没有__dict__属性，惊不惊喜~意不意外~')
    new = DotDict(old)
    print(new, type(new))
    print(new.__dict__)
    print(new.a)
    print(new.b)
    print(new.c)

    xx = DotDict(f=4, y=5)
    print(xx.f)

    object_dict = ObjectDict(old)
    print(object_dict.a)
    print(object_dict.b)
    print(object_dict.e.e_1)
    print(object_dict.e.e_2)